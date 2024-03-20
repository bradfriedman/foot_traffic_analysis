import json
import logging
from statistics import median

from django.conf import settings
from django.db.models import Avg, StdDev, Variance
from django.http import HttpResponse
from django.shortcuts import render

from fuzzywuzzy import fuzz, process

from langchain.output_parsers import XMLOutputParser
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI
import pandas as pd

from .utils.enums import LLMChoice
from .utils.llms import get_llm

from .forms import UserQueryForm

from .models import FootTraffic

from . import prompts


logger = logging.getLogger(__name__)


class AnalysisResult:
  def __init__(self, response: str, monthly_averages: pd.Series = None):
    self.response = response
    self.monthly_averages = monthly_averages


def analyze_view(request) -> HttpResponse:
  if request.method == 'POST':
    form = UserQueryForm(request.POST)
    if form.is_valid():
      user_query = form.cleaned_data['query']
      llm_choice_value = form.cleaned_data['llm_choice']
      llm_choice = LLMChoice(llm_choice_value)

      logger.debug(f"User query: {user_query}")

      logger.debug("Running chain...")
      analysis_result = run_analysis(user_query, llm_choice=llm_choice)
      response = analysis_result.response
      monthly_averages = analysis_result.monthly_averages

      if monthly_averages is not None:
        chart_labels = json.dumps(
            list(monthly_averages.index.strftime('%Y-%m')))
        chart_data = json.dumps(list(monthly_averages.values))
      else:
        chart_labels = None
        chart_data = None

      return render(
          request,
          'index.html',
          {
              'form': form,
              'insights_summary': response,
              'chart_labels': chart_labels,
              'chart_data': chart_data,
              'llm_choice': llm_choice_value,
          }
      )
  else:
    form = UserQueryForm()

  return render(request, 'index.html', {'form': form})


def run_analysis(query: str, llm_choice: LLMChoice = LLMChoice.CHATGPT45) -> AnalysisResult:
  llm = get_llm(llm_choice)

  # *** Filtering ***
  parser = XMLOutputParser(tags=["result", "shopping_center", "city"])
  filtering_prompt = PromptTemplate.from_template(
      template=prompts.FILTERING_PROMPT,
      partial_variables={
          "format_instructions": parser.get_format_instructions()},
  )
  chain = filtering_prompt | llm | parser
  output = chain.invoke({"query": query})

  shopping_center = output.get("result", [{}])[0].get("shopping_center")
  city = output.get("result", [{}, {}])[1].get("city")

  print(f"Shopping center: {shopping_center}, City: {city}")

  shopping_center_names = set(
      FootTraffic.objects.values_list('name', flat=True))

  if shopping_center:
    shopping_center_matches = process.extractBests(
        shopping_center, shopping_center_names, scorer=fuzz.ratio, score_cutoff=settings.MIN_RATIO)
    matched_names = [m[0] for m in shopping_center_matches]

    # Print the ratio scores for each possible shopping center name that exceeds MIN_RATIO
    if shopping_center_matches:
      print("Shopping Center Name Ratio Scores:")
      for m in shopping_center_matches:
        print(f"{m[0]}: {m[1]}")

      # Set shopping center to the best match
      shopping_center = matched_names[0]
    else:
      print("NO SHOPPING CENTERS FOUND")
      return AnalysisResult(
          f"No shopping center found with the name {shopping_center}. Please try again.")

  city_names = set(
      FootTraffic.objects.values_list('city', flat=True)
  )

  if city:
    city_matches = process.extractBests(
        city, city_names, scorer=fuzz.ratio, score_cutoff=settings.MIN_RATIO)
    matched_cities = [m[0] for m in city_matches]

    # Print the ratio scores for each possible city exceeds MIN_RATIO
    if city_matches:
      print("City Ratio Scores:")
      for m in city_matches:
        print(f"{m[0]}: {m[1]}")

      # Set city to the best match
      city = matched_cities[0]
    else:
      # If a city was extracted but does not match any in the database,
      # short circuit and return an error message
      print("NO CITIES FOUND")
      return AnalysisResult(
          f"Could not recognize the city {city}. Please try again.")

  print(f"Shopping center: {shopping_center}, City: {city}")

  # If not shopping center or city can be extracted, return an error message
  if not shopping_center and not city:
    return AnalysisResult("No shopping center or city could be extracted from the user query. Please try again.")

  # Select only the FootTraffic objects where the shopping center name is in
  # the matched names and the city is in the matched cities (if provided)
  filtered_ft = (FootTraffic.objects.filter(
      name=shopping_center, city=city) if city
      else FootTraffic.objects.filter(name=shopping_center)
  ).order_by('day')

  # If no rows were returned, return an error now
  if not filtered_ft:
    error_msg = f"No foot traffic data found for {
        shopping_center}{' in ' + city if city else ''}."
    return AnalysisResult(error_msg)

  # Check if there are multiple locations with the shopping center name
  cities_represented = set(filtered_ft.values_list('city', flat=True))
  multiple_locations = len(cities_represented) > 1
  if multiple_locations:
    # For now, return an error message if there are multiple locations asking
    # the user to specify the city
    print("WARNING: Multiple locations with the shopping center name found. ",
          f"({', '.join(cities_represented)})")
    return AnalysisResult(
        "Multiple locations with the shopping center name "
        f"{shopping_center} found ({', '.join(cities_represented)}). "
        "Please specify the city."
    )
  else:
    print("Only one location with the shopping center name found.")

  filtered_ft_str = '\n'.join(str(ft) for ft in filtered_ft)

  print(
      f"Filtered FootTraffic string starts with:\n\n{'\n'.join(filtered_ft_str.split('\n')[:5])}\n\n")

  # Collect some mathematical data to augment prompts
  ft_mean = filtered_ft.aggregate(Avg('ft'))['ft__avg']
  ft_median = median(filtered_ft.values_list('ft', flat=True))
  ft_stddev = filtered_ft.aggregate(StdDev('ft'))['ft__stddev']
  ft_variance = filtered_ft.aggregate(Variance('ft'))['ft__variance']

  # Calculate monthly averages
  monthly_averages = get_monthly_averages(filtered_ft)
  monthly_averages_str = '\n'.join(
      monthly_averages.to_string(header=False).split('\n')[:-1])
  print(f"Monthly averages:\n{monthly_averages_str}")

  # *** Trend Analysis ***
  parser = StrOutputParser()
  trend_analysis_prompt = PromptTemplate.from_template(
      template=prompts.TREND_ANALYSIS_PROMPT,
  )

  chain = trend_analysis_prompt | llm | parser
  trend_input = filtered_ft_str
  # print(f"Trend input: {trend_input}")
  trend_summary = chain.invoke(
      {
          "data_str": trend_input,
          "ft_mean": ft_mean,
          "ft_median": ft_median,
          "ft_stddev": ft_stddev,
          "ft_variance": ft_variance,
          "monthly_averages": monthly_averages_str,
      }
  )
  print(f"Output of trend analysis chain is\n\n{trend_summary}\n\n")

  # *** Anomaly Detection ***
  parser = StrOutputParser()
  anomaly_detection_prompt = PromptTemplate.from_template(
      template=prompts.ANOMALY_DETECTION_PROMPT,
  )

  chain = anomaly_detection_prompt | llm | parser
  anomaly_input = filtered_ft_str
  # print(f"Anomaly input: {anomaly_input}")
  anomalies_summary = chain.invoke(
      {
          "data_str": anomaly_input,
          "ft_mean": ft_mean,
          "ft_median": ft_median,
          "ft_stddev": ft_stddev,
          "ft_variance": ft_variance,
      }
  )
  print(f"Output of anomaly detection chain is:\n\n{anomalies_summary}\n\n")

  # *** Insights Generation ***
  parser = StrOutputParser()
  insights_generation_prompt = PromptTemplate.from_template(
      template=prompts.INSIGHTS_GENERATION_PROMPT,
  )

  chain = insights_generation_prompt | llm | parser

  # Get earliest and latest date of the dataset
  earliest_date = filtered_ft.earliest('day').day
  latest_date = filtered_ft.latest('day').day

  output = chain.invoke(
      {
          "trend_summary": trend_summary,
          "anomalies_summary": anomalies_summary,
          "earliest_date": earliest_date.strftime("%b %d, %Y"),
          "latest_date": latest_date.strftime("%b %d, %Y"),
      }
  )
  print(f"Output of insights generation chain is:\n\n{output}\n\n")

  return AnalysisResult(output, monthly_averages)


def get_monthly_averages(filtered_ft) -> pd.Series:
  data = filtered_ft.values_list('day', 'ft')
  dates = [d[0] for d in data]
  foot_traffic_counts = [ft[1] for ft in data]

  # Convert to DataFrame
  df = pd.DataFrame({'date': dates, 'foot_traffic_count': foot_traffic_counts})
  df['date'] = pd.to_datetime(df['date'])
  df = df.set_index('date')

  # Calculate monthly averages
  return df['foot_traffic_count'].resample('ME').mean()
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt
from django.db.models.query import QuerySet
from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for server-side rendering


def create_chart(ft_objs: QuerySet) -> str:
  """
  Creates a matplotlib chart from the given FootTraffic objects.
  """
  # Get the data from the FootTraffic objects
  data = ft_objs.values_list('day', 'ft')
  dates = [d[0] for d in data]
  foot_traffic_counts = [ft[1] for ft in data]

  # Convert to DataFrame
  df = pd.DataFrame({'date': dates, 'foot_traffic_count': foot_traffic_counts})
  df['date'] = pd.to_datetime(df['date'])
  df = df.set_index('date')

  # Calculate monthly averages
  monthly_averages = df['foot_traffic_count'].resample('ME').mean()

  # Create the chart
  fig, ax = plt.subplots(figsize=(8, 6))
  ax.plot(monthly_averages.index, monthly_averages.values)
  ax.set_xlabel('Date')
  ax.set_ylabel('Foot Traffic')
  ax.set_title('Foot Traffic Over Time (Monthly Averages)')

  # Convert the chart to a base64-encoded string
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_png = buffer.getvalue()
  chart_base64 = base64.b64encode(image_png).decode('utf-8')

  return chart_base64

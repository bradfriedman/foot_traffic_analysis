import datetime
import logging

from django.db.models.query import QuerySet
import numpy as np
from scipy.stats import zscore

logger = logging.getLogger(__name__)


def calculate_daily_z_scores(queryset: QuerySet) -> dict:
  '''
  Calculate the z-scores for the foot traffic values in the queryset.

  Returns a dictionary where the keys are the dates and the values are tuples
  of the foot traffic value and the z-score for that value.

  :param queryset: A Django QuerySet of FootTraffic objects
  :return: A dictionary of dates to tuples of foot traffic values and z-scores
  '''
  ft_values = queryset.values_list('ft', flat=True)
  ft_array = np.array(list(ft_values))
  z_scores = zscore(ft_array)
  logger.debug(logger.debug("Z SCORES = ", z_scores))

  for i, z_score in enumerate(z_scores):
    row = queryset[i]
    logger.debug("Row:", row)
    logger.debug("Z-score:", z_score)

  logger.debug("Mean Z-score:", np.mean(z_scores))
  logger.debug("Standard Deviation of Z-scores:", np.std(z_scores))
  z_score_dict = {}
  for i, z_score in enumerate(z_scores):
    row = queryset[i]
    date = row.day
    ft = row.ft
    z_score_dict[date] = (ft, z_score)

  return z_score_dict


def calculate_weekly_z_scores(queryset: QuerySet) -> dict:
  '''
  Calculate the z-scores for the foot traffic values in the queryset at the
  weekly level.

  Returns a dictionary where the keys are the ISO year and week, and the values
  are tuples of the foot traffic value and the z-score for that value.

  :param queryset: A Django QuerySet of FootTraffic objects
  :return: A dictionary of ISO year and week to tuples of foot traffic values
           and z-scores
  '''
  ft_values = queryset.values_list('avg_ft', flat=True)
  ft_array = np.array(list(ft_values))
  z_scores = zscore(ft_array)
  z_score_dict = {}
  for i, z_score in enumerate(z_scores):
    row = queryset[i]
    logger.debug("Row:", row)
    logger.debug("Z-score:", z_score)
    ft = row['avg_ft']
    iso_year = row['year']
    iso_week = row['week']
    z_score_dict[(iso_year, iso_week)] = (ft, z_score)
    logger.debug(f"{iso_to_gregorian(iso_year, iso_week)}: {
                 ft} (Z-score: {z_score})")
  return z_score_dict


def get_anomalies(z_score_dict: dict, threshold: float = 2.0) -> dict:
  '''
  Get anomalies from the z-score dictionary based on a threshold.

  Returns a dictionary of dates to tuples of foot traffic values and z-scores
  for values that exceed the threshold.

  :param z_score_dict: A dictionary of dates to tuples of foot traffic values
                       and z-scores
  :param threshold: The z-score threshold for determining anomalies

  :return: A dictionary of dates to tuples of foot traffic values and z-scores
           for anomalies
  '''
  anomalies = {}
  for k, (ft, z_score) in z_score_dict.items():
    if abs(z_score) > threshold:
      anomalies[k] = (ft, z_score)
  return anomalies


def django_weekday_to_str(weekday: int) -> str:
  '''
  Convert Django weekday integer to string.

  :param weekday: Django weekday integer (0-6)
  :return: String representation of the weekday
  '''
  if not 1 <= weekday <= 7:
    raise ValueError("Weekday must be between 1 and 7")
  weekdays = ['Sunday', "Monday", "Tuesday",
              "Wednesday", "Thursday", "Friday", "Saturday"]
  return weekdays[weekday-1]


def iso_to_gregorian(iso_year, iso_week):
  '''
  Function to convert ISO year and week to the first day of that week (Monday)
  in the Gregorian calendar.

  :param iso_year: The ISO year
  :param iso_week: The ISO week
  :return: The first day of the week in the Gregorian calendar
  '''
  "The inverse of `datetime.date.isocalendar()`"
  fourth_jan = datetime.date(iso_year, 1, 4)
  _, fourth_jan_week, fourth_jan_day = fourth_jan.isocalendar()
  return fourth_jan + datetime.timedelta(days=1-fourth_jan_day, weeks=iso_week-fourth_jan_week)

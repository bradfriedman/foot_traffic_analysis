from django.db.models.query import QuerySet
import numpy as np
from scipy.stats import zscore


def calculate_z_scores(queryset: QuerySet) -> dict:
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
  print("Z SCORES = ", z_scores)

  for i, z_score in enumerate(z_scores):
    row = queryset[i]
    print("Row:", row)
    print("Z-score:", z_score)

  print("Mean Z-score:", np.mean(z_scores))
  print("Standard Deviation of Z-scores:", np.std(z_scores))
  z_score_dict = {}
  for i, z_score in enumerate(z_scores):
    row = queryset[i]
    date = row.day
    ft = row.ft
    z_score_dict[date] = (ft, z_score)

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
  for date, (ft, z_score) in z_score_dict.items():
    if abs(z_score) > threshold:
      anomalies[date] = (ft, z_score)
  return anomalies

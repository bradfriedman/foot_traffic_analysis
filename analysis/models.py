from django.db import models

from .utils.enums import DayOfWeek


class FootTraffic(models.Model):
  day = models.DateField(help_text='The date of the record')
  shopping_center_id = models.CharField(
      max_length=255, help_text='The unique identifier of the shopping center')
  name = models.CharField(
      max_length=255, help_text='The name of the shopping center', db_index=True)
  ft = models.IntegerField(
      help_text='The foot traffic at the shopping center', null=True)
  state = models.CharField(
      max_length=2, help_text='The state code where the shopping center is located', db_index=True, null=True)
  city = models.CharField(
      max_length=255, help_text='The city where the shopping center is located', db_index=True, null=True)
  formatted_address = models.CharField(
      max_length=255, help_text='The full address of the shopping center', db_index=True, null=True)
  lon = models.DecimalField(max_digits=10, decimal_places=8,
                            help_text='The longitude coordinate of the shopping center', null=True)
  lat = models.DecimalField(max_digits=10, decimal_places=8,
                            help_text='The latitude coordinate of the shopping center', null=True)

  def __str__(self) -> str:
    return f"Name: {self.name}, Day: {self.day} ({DayOfWeek(self.day.weekday()).name}), City: {self.city}, State: {self.state}, Foot Traffic: {self.ft}"

  class Meta:
    unique_together = ('day', 'shopping_center_id')

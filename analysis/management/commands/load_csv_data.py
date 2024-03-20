import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from analysis.models import FootTraffic


class Command(BaseCommand):
  help = 'Loads data from a CSV file into the FootTraffic model'

  def add_arguments(self, parser) -> None:
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')

  @transaction.atomic
  def handle(self, *args, **options) -> None:
    csv_file = options['csv_file']
    with open(csv_file, 'r') as file:
      reader = csv.DictReader(file)
      foot_traffic_list = []
      for row in reader:
        foot_traffic = FootTraffic(
            day=row['day'],
            shopping_center_id=row['id'],
            name=row['name'],
            ft=row['ft'],
            state=row['state'],
            city=row['city'],
            formatted_address=row['formatted_address'],
            lon=row['lon'],
            lat=row['lat']
        )
        foot_traffic_list.append(foot_traffic)

      FootTraffic.objects.bulk_create(foot_traffic_list)

    self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))

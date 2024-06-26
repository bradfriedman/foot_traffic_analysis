# Generated by Django 5.0.3 on 2024-03-18 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootTraffic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(help_text='The date of the record')),
                ('shopping_center_id', models.CharField(help_text='The unique identifier of the shopping center', max_length=255)),
                ('name', models.CharField(help_text='The name of the shopping center', max_length=255)),
                ('ft', models.IntegerField(help_text='The foot traffic at the shopping center', null=True)),
                ('state', models.CharField(help_text='The state code where the shopping center is located', max_length=2, null=True)),
                ('city', models.CharField(help_text='The city where the shopping center is located', max_length=255, null=True)),
                ('formatted_address', models.CharField(help_text='The full address of the shopping center', max_length=255, null=True)),
                ('lon', models.DecimalField(decimal_places=8, help_text='The longitude coordinate of the shopping center', max_digits=10, null=True)),
                ('lat', models.DecimalField(decimal_places=8, help_text='The latitude coordinate of the shopping center', max_digits=10, null=True)),
            ],
            options={
                'unique_together': {('day', 'shopping_center_id')},
            },
        ),
    ]

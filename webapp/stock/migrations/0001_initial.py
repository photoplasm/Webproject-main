# Generated by Django 5.0.6 on 2024-09-23 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(default='No description provided.')),
                ('material', models.CharField(default='Unknown', max_length=255)),
                ('dimensions', models.CharField(default='Not specified', max_length=100)),
                ('color', models.CharField(default='White', max_length=50)),
                ('image_url', models.URLField()),
            ],
        ),
    ]

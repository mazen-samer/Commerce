# Generated by Django 4.1.1 on 2022-09-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_listings_alter_bid_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(blank=True),
        ),
    ]
# Generated by Django 2.2 on 2019-05-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_comment_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_name', models.CharField(max_length=50)),
                ('img_path', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=50)),
                ('location_coordinat', models.CharField(max_length=50)),
                ('location_desc', models.CharField(max_length=50)),
                ('user_id', models.IntegerField(max_length=50)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=50)),
                ('map_id', models.IntegerField()),
            ],
        ),
    ]
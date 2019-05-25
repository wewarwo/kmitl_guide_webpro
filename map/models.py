from django.db import models

# Create your models here.

class location(models.Model):
    types = (
        ('toilet', 'Toilet'),
        ('parking', 'Parking'),
        ('faculty', 'Faculty'),
        ('cafeteria', 'Cafeteria'),
        ('other', 'Other'),
    )
    zone_id = models.IntegerField()
    location_name = models.CharField(max_length=50)
    coordinate = models.CharField(max_length=50)
    descript = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=types, default='other')
    img_path = models.CharField(max_length=255)

class comment(models.Model):
    location_id = models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    create_date = models.DateTimeField()

class zone(models.Model):
    zone_name = models.CharField(max_length = 50)
    map_id = models.IntegerField()

class request(models.Model):
    location_name = models.CharField(max_length = 50)
    location_coordinat = models.CharField(max_length = 50)
    location_desc = models.CharField(max_length = 50)
    user_id = models.IntegerField()
    date_time = models.DateTimeField()

class map(models.Model):
    map_name = models.CharField(max_length=50)
    img_path = models.CharField(max_length = 50)

class contact(models.Model):
    subject = models.CharField(max_length=50)
    Subject_type = models.CharField(max_length = 50)
    Location = models.CharField(max_length = 50)
    Description = models.CharField(max_length = 100)

class question(models.Model):
    user_id = models.IntegerField()
    question = models.CharField(max_length = 50)
    answer = models.CharField(max_length=50)
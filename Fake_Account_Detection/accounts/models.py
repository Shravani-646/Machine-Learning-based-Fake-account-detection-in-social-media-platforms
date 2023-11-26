from django.db import models

# Create your models here.
class FeatureSet(models.Model):
    LANGUAGE_CHOICES = (
        ('en','English'),
        ('de','German'),
        ('es','Spanish'),
        ('fr','French'),
        ('gl','Galician'),
        ('it','Italian'),
        ('nl','Dutch'),
        ('tr','Turkish')
    )

    statuses_count = models.IntegerField()
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    favourites_count = models.IntegerField()
    listed_count = models.IntegerField()
    geo_enabled = models.BooleanField()
    user_profile_background_image = models.BooleanField()
    language = models.CharField(max_length=20,choices=LANGUAGE_CHOICES,default='English')


class CloneFeatureSet(models.Model):
        LANGUAGE_CHOICES = (
        ('en','English'),
        ('de','German'),
        ('es','Spanish'),
        ('fr','French'),
        ('gl','Galician'),
        ('it','Italian'),
        ('nl','Dutch'),
        ('tr','Turkish')
    )
        name = models.CharField(max_length=255)
        screen_name = models.CharField(max_length=255)
        language = models.CharField(max_length=20,choices=LANGUAGE_CHOICES,default='English')
        location = models.CharField(max_length=255)
        

    
class UserInput(models.Model):
    profile_url = models.CharField(max_length=255)


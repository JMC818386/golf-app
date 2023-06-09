from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    
    def __str__(self):
        return self.username

class Course(models.Model):
    name = models.CharField(max_length=50)
    par = models.IntegerField()

    def __str__(self):
        return f'{self.name}, {self.par}'

class Hole(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    number = models.IntegerField()
    par = models.IntegerField()
    distance = models.IntegerField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)
   
    def __str__(self):
        return f'{self.course}, {self.par}, {self.distance}, {self.number}'

class Round(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now, null=True)
    round_length = models.IntegerField(null=True)
    total_score = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user}, {self.course}, {self.date}, {self.round_length}, {self.total_score}'

class HoleScore(models.Model):
    hole_round = models.ForeignKey('Round', on_delete=models.CASCADE, null=True)
    hole = models.ForeignKey('Hole', on_delete=models.CASCADE, null=True)
    strokes = models.IntegerField(null=True)
    swings = models.IntegerField(null=True)
    putts = models.IntegerField(null=True)
   
    def __str__(self):
        return f'{self.hole_round}, {self.hole}, {self.strokes}, {self.swings}, {self.putts}'
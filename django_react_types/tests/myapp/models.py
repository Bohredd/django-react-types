from django.db import models

class ExampleModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class AnotherModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class AnotherModel2(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    another_model = models.ForeignKey(AnotherModel, on_delete=models.CASCADE)
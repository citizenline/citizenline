from django.db import models


class Texttype(models.Model):
  name = models.CharField(max_length=200)

class Improvetext(models.Model):
  texttype = models.ForeignKey(Texttype, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  slug = models.CharField(max_length=200)
  body = models.CharField(max_length=2000)
  pub_date = models.DateTimeField('date published')

class Comment(models.Model):
  improvetext = models.ForeignKey(Improvetext, on_delete=models.CASCADE)
  author = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  body = models.CharField(max_length=2000)
  notify = models.BooleanField(default=True)

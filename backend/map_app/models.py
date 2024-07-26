from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    polygon = models.JSONField()  # MySQLではJSONFieldを使用

    def __str__(self):
        return self.name

class Vote(models.Model):
    candidate_name = models.CharField(max_length=255)
    party_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    votes = models.IntegerField()
    election_date = models.DateField(default='2000-01-01')
    region = models.CharField(max_length=255, default='Tokyo')

    def __str__(self):
        return f"{self.candidate_name} ({self.party_name}) - {self.city}: {self.votes} votes on {self.election_date} in {self.region}"

class PopulationDistribution(models.Model):
    region_code = models.CharField(max_length=10)
    region = models.CharField(max_length=100)
    age_group = models.CharField(max_length=20)
    total_population = models.IntegerField()
    total_men = models.IntegerField()
    total_women = models.IntegerField()
    japanese_total = models.IntegerField()
    japanese_men = models.IntegerField()
    japanese_women = models.IntegerField()
    foreign_total = models.IntegerField()
    foreign_men = models.IntegerField()
    foreign_women = models.IntegerField()

    def __str__(self):
        return f"{self.region} - {self.age_group}"
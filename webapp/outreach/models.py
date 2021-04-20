from django.db import models


class Ranking(models.Model):
    name = models.CharField(max_length=127, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Firm(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    city_name = models.CharField(max_length=150, default="")
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=150, null=True)
    website = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=150, null=True)
    fax_number = models.CharField(max_length=150, null=True)
    firm_rankings = models.ManyToManyField(Ranking, related_name="firm_rankings")
    top_tier_firm_rankings = models.ManyToManyField(Ranking, related_name="top_tier_firm_rankings")

    def __str__(self):
        return self.name


class Attorney(models.Model):
    name = models.CharField(max_length=127, db_index=True, unique=True)
    firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)
    email = models.CharField(max_length=127, null=True)
    phone_number = models.CharField(max_length=127, null=True)
    picture = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} {self.firm_name}"

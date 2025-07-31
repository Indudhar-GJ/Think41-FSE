from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DistributionCenter(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"Distribution Center {self.id}"


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    distribution_center = models.ForeignKey(
        DistributionCenter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        ordering = ['name']

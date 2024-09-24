from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='No description provided.')  # Default description
    material = models.CharField(max_length=255, default='Unknown')  # Default material
    dimensions = models.CharField(max_length=100, default='Not specified')  # Default dimensions
    color = models.CharField(max_length=50, default='White')  # Default value is "White"
    image_url = models.URLField()  # Image URL of the product

    def __str__(self):
        return self.name

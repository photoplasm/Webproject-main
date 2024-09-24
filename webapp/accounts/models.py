from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='No description provided.')  # Default description
    material = models.CharField(max_length=255, default='Unknown')  # Default material
    dimensions = models.CharField(max_length=100, default='Not specified')  # Default dimensions
    color = models.CharField(max_length=50, default='White')  # Default value is "White"
    image_url = models.URLField()  # Image URL of the product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars"
    def __str__(self):
        return self.name

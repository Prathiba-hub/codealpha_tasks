from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

class Order(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    products = models.ManyToManyField(Product)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.name
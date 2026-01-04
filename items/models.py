from django.db import models
from django.contrib.auth.models import User


#Items Database

class Item(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('returned', 'Returned'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='items'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


#Claims Database
class Claim(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.title} - {self.claimant.username}"

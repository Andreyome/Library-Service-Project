from django.db import models

class Book(models.Model):
    class Choices(models.TextChoices):
        HARD = "HARD", "Hard cover"
        SOFT = "SOFT", "Soft cover"
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=4, choices=Choices.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title}"

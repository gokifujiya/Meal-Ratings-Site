from django.db import models

class Meal(models.Model):
    MORNING, AFTERNOON, EVENING = 1, 2, 3
    MEALTIME_CHOICES = (
        (MORNING, "morning"),
        (AFTERNOON, "afternoon"),
        (EVENING, "evening"),
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    imageUrl = models.CharField(max_length=64)  # "1.jpeg", ...
    countryOfOrigin = models.CharField(max_length=64)
    typicalMealTime = models.IntegerField(choices=MEALTIME_CHOICES)
    dateAdded = models.DateTimeField()

    def __str__(self):
        return self.name

class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="ratings")
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    dateOfRating = models.DateTimeField()

    def __str__(self):
        return f"{self.meal} — {self.rating}"

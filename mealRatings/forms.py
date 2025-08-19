from django import forms
from .models import Meal, MealRating

class NewMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        # dateAdded is set in the view to "now"
        fields = ["name","description","imageUrl","countryOfOrigin","typicalMealTime"]
        widgets = {
            "imageUrl": forms.TextInput(attrs={"pattern": r"^\d+\.jpeg$", "title": "e.g. 7.jpeg"}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = MealRating
        fields = ["rating"]  # dateOfRating set in view to "now"
        widgets = {
            # nice slider
            "rating": forms.NumberInput(attrs={"type":"range","min":"0","max":"5","step":"0.01"})
        }

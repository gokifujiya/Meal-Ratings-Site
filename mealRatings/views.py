from datetime import timedelta
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Meal
from .forms import NewMealForm, RatingForm

IMG_BASE = "https://recursionist.io/img/dashboard/lessons/quickstart/"

def _with_stats(qs):
    return qs.annotate(avg_rating=Avg("ratings__rating"), votes=Count("ratings"))

def index(request):
    # POST => create a new meal, dateAdded = now, then show landing again
    if request.method == "POST":
        form = NewMealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.dateAdded = timezone.now()
            meal.save()
            return redirect(reverse("meals:index"))
    else:
        form = NewMealForm()

    # 3 images from each category
    morning = _with_stats(Meal.objects.filter(typicalMealTime=Meal.MORNING)).order_by("-dateAdded")[:3]
    afternoon = _with_stats(Meal.objects.filter(typicalMealTime=Meal.AFTERNOON)).order_by("-dateAdded")[:3]
    evening = _with_stats(Meal.objects.filter(typicalMealTime=Meal.EVENING)).order_by("-dateAdded")[:3]

    # recently added within last 90 days
    cutoff = timezone.now() - timedelta(days=90)
    recent = _with_stats(Meal.objects.filter(dateAdded__gte=cutoff)).order_by("-dateAdded")[:3]

    # top rated (avg >= 4.5)
    top = [m for m in _with_stats(Meal.objects.all()) if (m.avg_rating or 0) >= 4.5][:3]

    return render(request, "mealRatings/index.html", {
        "form": form,
        "IMG_BASE": IMG_BASE,
        "morning": morning, "afternoon": afternoon, "evening": evening,
        "recent": recent, "top": top,
    })

def categoryList(request, category: str):
    # header links include landing & all categories
    qs = _with_stats(Meal.objects.all())
    cutoff = timezone.now() - timedelta(days=90)

    if category == "morning":
        qs = qs.filter(typicalMealTime=Meal.MORNING)
    elif category == "afternoon":
        qs = qs.filter(typicalMealTime=Meal.AFTERNOON)
    elif category == "evening":
        qs = qs.filter(typicalMealTime=Meal.EVENING)
    elif category == "recent":
        qs = qs.filter(dateAdded__gte=cutoff)
    elif category == "top":
        qs = qs.filter(ratings__rating__gte=4.5)  # coarse filter; we’ll sort by avg below
    else:
        # unknown category => 404
        from django.http import Http404
        raise Http404("Unknown category")

    # sorting
    sort = request.GET.get("sort", "recent")
    if sort == "recent":
        qs = qs.order_by("-dateAdded")
    elif sort == "top":
        qs = qs.order_by("-avg_rating")
    elif sort == "country":
        qs = qs.order_by("countryOfOrigin","name")

    meals = qs
    return render(request, "mealRatings/category_list.html", {
        "category": category,
        "meals": meals,
        "IMG_BASE": IMG_BASE,
        "sort": sort,
    })

def detail(request, pk: int):
    meal = get_object_or_404(_with_stats(Meal.objects.all()), pk=pk)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.meal = meal
            rating.dateOfRating = timezone.now()
            rating.save()
            return redirect(reverse("meals:detail", args=[pk]))
    else:
        form = RatingForm()

    return render(request, "mealRatings/detail.html", {
        "meal": meal, "IMG_BASE": IMG_BASE, "form": form
    })

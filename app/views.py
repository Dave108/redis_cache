from django.shortcuts import render
from .models import TestModel
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def home_view(request):
    search_obj = request.GET.get('search')
    if cache.get(search_obj):
        search_result = cache.get(search_obj)
        print("cache result")
    else:
        if search_obj:
            search_result = TestModel.objects.filter(
                Q(name__icontains=search_obj) | Q(description__icontains=search_obj))
            print("DB Result")
            cache.set(search_obj, search_result, timeout=CACHE_TTL)
        else:
            search_result = TestModel.objects.all()
    context = {
        "objects": search_result,
    }
    return render(request, 'home.html', context)

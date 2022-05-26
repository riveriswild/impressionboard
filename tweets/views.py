import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url  # INFO safe urls for forms

from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS  # info for safe urls


def home_view(request, *args, **kwargs):
    print(args, kwargs)
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)  # we initialize form class with data or not (if there is data - send to form or send none)
    # print('post data is', request.POST)
    next_url = request.POST.get('next') or None
    # print('next url is', next_url)
    if form.is_valid():
        obj = form.save(commit=False)   # if form valid - save
        # do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)   # 201 for created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):  # INFO safe url for forms
            return redirect(next_url)
        form = TweetForm()  # reinitialise new form
        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form},)


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    # tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 120)} for x in qs]  # replaced by
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    return json data
    """
    print(args, kwargs)
    data = {
        "id": tweet_id,
        # "content": obj.content,
        # "image_path": obj.image.url,
        # 'status': 200,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content   # if found put content of object into content of data
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)
    # return HttpResponse(f"<h1>Hello! {tweet_id} - {obj.content}</h1>")

# Create your views here.

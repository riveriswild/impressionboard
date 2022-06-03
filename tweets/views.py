import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url  # INFO safe urls for forms

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import Tweet
from .forms import TweetForm
from .serializers import (
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS  # info for safe urls


def home_view(request, *args, **kwargs):
    print(request.user or None)
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])  # http method == post
# @authentication_classes([SessionAuthentication])   # TODO do I even need this?
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        # print(serializer.data)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    Shows tweet details
    """
    qs = Tweet.objects.filter(id=tweet_id)   # TODO check if works with get
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    """
    Checks if user is author of the tweet, if so, deletes tweet
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)   # check if user is author
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet deleted"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
    id is required
    Action options: like, unlike, retweet
    """
    # print(request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    """
    Shows list view of all tweets
    """
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    # print(serializer.data)
    return Response(serializer.data)


# def tweet_create_view_pure_django(request, *args, **kwargs):
#     user = request.user  # to check user
#     if not request.user.is_authenticated:  # check if user is authenticated; for http request
#         user = None
#         if request.is_ajax():  # for ajax request
#             return JsonResponse({}, status=401)  # 401 - not authorized
#         return redirect(settings.LOGIN_URL)
#     form = TweetForm(
#         request.POST or None)  # we initialize form class with data or not (if there is data - send to form or send none)
#     # print('post data is', request.POST)
#     next_url = request.POST.get('next') or None
#     # print('next url is', next_url)
#     if form.is_valid():
#         obj = form.save(commit=False)  # if form valid - save
#         obj.user = user
#         # do other form related logic
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201)  # 201 for created items
#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):  # INFO safe url for forms
#             return redirect(next_url)
#         form = TweetForm()  # reinitialise new form
#         if form.errors:
#             if request.is_ajax():
#                 return JsonResponse(form.errors, status=400)
#     return render(request, 'components/form.html', context={"form": form}, )
#
#
# def tweet_list_view_pure_django(request, *args, **kwargs):
#     qs = Tweet.objects.all()
#     tweets_list = [x.serialize() for x in qs]
#     # tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 120)} for x in qs]  # replaced by
#     data = {
#         "response": tweets_list
#     }
#     return JsonResponse(data)
#
#
# def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
#     """
#     REST API VIEW
#     return json data
#     """
#     print(args, kwargs)
#     data = {
#         "id": tweet_id,
#         # "content": obj.content,
#         # "image_path": obj.image.url,
#         # 'status': 200,
#     }
#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data['content'] = obj.content  # if found put content of object into content of data
#     except:
#         data['message'] = "Not found"
#         status = 404
#     return JsonResponse(data, status=status)
#     # return HttpResponse(f"<h1>Hello! {tweet_id} - {obj.content}</h1>")
#
# # Create your views here.

from django.contrib import admin

from .models import Tweet, TweetLike


class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):    # search in admin panel
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']     # str - tweet object, user - tweet user
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Tweet

admin.site.register(Tweet,TweetAdmin)
# Register your models here.

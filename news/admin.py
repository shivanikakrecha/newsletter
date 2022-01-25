from django.contrib import admin
from news.models import *

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
	list_display = ('news_headline', "total_autheticities", "user_authenticate", "user_not_authenticate")

	def total_autheticities(self, obj):
		# This method represents the total user count.
		return NewsAuthenticity.objects.filter(news=obj).count()

	def user_not_authenticate(self, obj):
		# This method represents the total count of news authenticate by the users.
		return NewsAuthenticity.objects.filter(news=obj, is_news_autheticate=False).count()

	def user_authenticate(self, obj):
		# This method represents the total count of not news authenticate by the users.
		return NewsAuthenticity.objects.filter(news=obj, is_news_autheticate=True).count()

admin.site.register(News, NewsAdmin)
admin.site.register(NewsAuthenticity)
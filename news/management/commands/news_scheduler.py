from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from news.models import News, NewsAuthenticity
from datetime import datetime

import requests
import json


class Command(BaseCommand):
	help = 'This command will fetch the latest news from the api portal.'

	def handle(self, *args, **options):
		
		api_key = settings.NEWS_APIKEY
		country = "in"
		categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
		# https://newsapi.org/v2/top-headlines?country=de&category=business&apiKey=e60385d8cafe4f708ada5062100687e6


		for category in categories:
			api_endpoint = settings.NEWS_URL + '/top-headlines/?country={}&category={}&apiKey={}'.format(
				country, category, api_key)

			response = requests.get(api_endpoint)

			if response.request.method == 'GET' and response.status_code == 200:
				response_data = json.loads(response.text)

				if bool(response_data):
					articles = response_data.get('articles')

					today_news = [
						news for news in articles
						if datetime.strptime(news.get('publishedAt').split(
							'T')[0] , '%Y-%m-%d').date() == datetime.now().date()
					]

					with transaction.atomic():

						news_objects = [

							News(
								author=news.get('author', None),
								news_description=news.get('description', None),
								news_headline=news.get('title', ""),
								category=category,
								source_url=news.get('url', None),
								api_endpoint=api_endpoint
							)
							for news in today_news
						]

						News.objects.bulk_create(news_objects)

			else:
				pass


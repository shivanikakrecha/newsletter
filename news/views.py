from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from news.models import NewsAuthenticity, News
from django.contrib.auth.models import User
from rest_framework import status


class NewsUserAuthenticity(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, news_id, user_id):
        try:

            user_id = int(user_id) # Convert in integer
            news_id = int(news_id) # Convert in integer

            if news_id and user_id :

                # Find user object to get preferencies.
                user_object = User.objects.get(id=user_id)

                # Get news object
                news_object = NewsAuthenticity.objects.get(
                    news__id=news_id,
                    user__id=user_id
                )

                if not news_object.news.category in user_object.fetch_userpreferencies(): 
                    return Response({"detail": "Not authorized to perform this action!"},
                            status=status.HTTP_401_UNAUTHORIZED)

                # User approval 
                news_object.is_news_autheticate = True
                news_object.save()

                response = dict()
                response["detail"] = "Validate!"

                return Response(response, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "Invalid parameters."},
                            status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({"detail": "Invalid parameters."},
                            status=status.HTTP_401_UNAUTHORIZED)

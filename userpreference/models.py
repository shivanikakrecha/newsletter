from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True,
                                      verbose_name='Created At')
    modified_at = models.DateTimeField(auto_now=True, db_index=True,
                                       verbose_name='Modified At')

    class Meta:
        abstract = True


class UserPreference(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Preference = models.CharField(max_length=30)

	def __str__(self):
		return self.Preference


def fetch_userpreferencies(self):
  return UserPreference.objects.filter(user__id=self.id).values_list(
    'Preference', flat=True)

User.add_to_class("fetch_userpreferencies",fetch_userpreferencies)

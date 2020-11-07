from django.db import models
from django.urls import reverse

# Create your models here.
class UserPreference(models.Model):

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="preferences")
    category = models.ForeignKey("news.NewsCategory", on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="pref_category")
    provider = models.ForeignKey("news.NewsProvider", on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="pref_provider")

    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self):
        return self.user.username + "'s preferences"

    def get_absolute_url(self):
        return reverse("news:accounts:preferences", kwargs={"pk": self.pk})

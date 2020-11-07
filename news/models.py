from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class NewsProvider(models.Model):
    """
    create a NewsProvider object
    """

    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    website = models.URLField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = "News Provider"
        verbose_name_plural = "News Providers"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(NewsProvider, self).save(*args, **kwargs)


class NewsCategory(models.Model):
    """
    create a NewsCategory object
    """

    category = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(NewsCategory, self).save(*args, **kwargs)


class News(models.Model):
    """
    create a News object
    """

    provider = models.ForeignKey("news.NewsProvider", on_delete=models.CASCADE,
                                related_name="news")
    category = models.ForeignKey("news.NewsCategory", on_delete=models.CASCADE,
                                null=True, related_name="news")
    thumbnail = models.URLField(max_length=500, null=True)
    headline = models.CharField(max_length=250)
    url = models.URLField(max_length=500, unique=True)
    published_on = models.DateTimeField()
    story_excerpt = models.CharField(max_length=500, blank=True)
    story_content = models.TextField()
    story_img = models.URLField(max_length=500, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-published_on"]

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        super(News, self).save(*args, **kwargs)
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="featured_images/", null=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    short_description = models.CharField(max_length=150, blank=True)
    content = HTMLField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name="posts")
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Tag(DateTimeModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('post', 'user')

class Category(DateTimeModel):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Comment(DateTimeModel):
    comment_text = models.CharField(max_length=100)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="comments")

    class Meta:
        unique_together = ('post', 'user')

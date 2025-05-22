from django.db import models
from django.db.models.aggregates import Count
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def post_count(self):
        return self.blogs.count()

    @classmethod
    def get_categories_with_count(cls):
        return cls.objects.annotate(post_count=Count('blogs'))
    


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    image = models.FileField(upload_to="media/images/", null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)  
        super().save(*args, **kwargs)

class Contact(models.Model):
    phone = models.CharField(max_length=20)
    email = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.email
    
class Service(models.Model):
    title = models.CharField(max_length=255)
    about = models.TextField()
    body = models.TextField()
    image = models.FileField(upload_to='media/service/images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Plan(models.Model):
    plan_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.plan_name

class Pricing(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='pricing_set', null=True, blank=True)
    sum = models.CharField(max_length=10)
    kerak = models.TextField(null=True, blank=True, unique=True)
    kerakmas = models.TextField(blank=True, unique=True)
    yearly_plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='yearly_pricing_set', null=True, blank=True)
    yearly_sum = models.CharField(max_length=10, null=True, blank=True, unique=True)
    yearly_kerak = models.TextField(null=True, blank=True, unique=True)
    yearly_kerakmas = models.TextField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.sum

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

    def children(self):
        return self.replies.all().order_by('created_at')

    @property
    def is_parent(self):
        return self.parent is None
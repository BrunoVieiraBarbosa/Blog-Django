from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, auto_created=True)
    thumb = models.ImageField(upload_to='posts/', blank=True)
    description = models.CharField(max_length=200)
    text = RichTextField()
    pub_date = models.DateField('publish date', auto_now_add=True)

    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.DO_NOTHING)

    previous_post = models.ForeignKey('self', related_name='previous_p', blank=True, null=True, on_delete=models.DO_NOTHING)
    next_post = models.ForeignKey('self', related_name='next_p', blank=True, null=True, on_delete=models.DO_NOTHING)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title



class LandingPage(models.Model):
    name = models.CharField(max_length=50, default="Pagina Principal")
    finished_project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.PROTECT, related_name="finished_project")
    ongoing_project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.PROTECT, related_name="ongoing_project")
    text_alt_project = models.CharField(blank=True, max_length=200)
    text_alt_project_in_progress = models.CharField(blank=True, max_length=200)

    def __str__(self) -> str:
        return "Landing Page"
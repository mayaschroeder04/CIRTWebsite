from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)
    # cat_id = models.IntegerField()
    cat_id = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE, db_column='cat_id')


    class Meta:
        db_table = 'subcategories'

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="documents")
    subcategory_id = models.IntegerField(null=True, blank=True)  # Keep it simple for now
    file_url = models.CharField(max_length=255)
    file_size = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return self.title

# class CustomeUser(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
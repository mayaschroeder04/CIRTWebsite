
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcategories'

    def __str__(self):
        return self.name

class Images(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
    file_size = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_user = models.IntegerField(null=True, blank=True)


class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    # subcategory_id = models.IntegerField(null=True, blank=True)  # You can improve this later with a proper FK
    file_url = models.CharField(max_length=255)
    file_size = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_user = models.IntegerField(null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="documents")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)  # Ensure this is defined

    STATUS = [
        ('approved', 'Approved' ),
        ('rejected', 'Rejected' ),
        ('pending', 'Pending' ),
    ]

    TYPE = [
        ('journal', 'Journal' ),
        ('image', 'Image' ),
    ]

    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    type = models.CharField(max_length=10, choices=TYPE, default='journal')

    def get_citation(self):
        # Generate MLA citation
        citation = f"{self.author}. \"{self.title}.\" *{self.category.name}*, {self.created_at.year}, http://UniversityOfTampaCirt/{self.file_url if self.file_url else 'No URL available'}."
        return citation

    class Meta:
        db_table = "documents"

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('reviewer', 'Reviewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    saved_documents = models.ManyToManyField('main.Document', blank=True, related_name='saved_by')
    groups = models.ManyToManyField(Group, blank=True, related_name="customuser_set")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="customuser_set")

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Journal(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)
    description = models.TextField()
    file_url = models.URLField()  # Or FileField if you're uploading actual files

    def __str__(self):
        return self.title
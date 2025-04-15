from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


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
    category_id = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE, db_column='category_id')

    class Meta:
        db_table = 'subcategories'

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="documents")
    subcategory_id = models.IntegerField(null=True, blank=True)  # You can improve this later with a proper FK
    file_url = models.CharField(max_length=255)
    file_size = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_user = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return self.title





class CustomUser(AbstractUser):
    saved_documents = models.ManyToManyField(Document, blank=True, related_name='saved_by')

    # Override groups field with a custom related_name to avoid clashes.
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Use a name that doesn't conflict with Group.user_set
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    # Override user_permissions field similarly.
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Use a custom related name as well
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return self.username

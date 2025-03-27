from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'categories'

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
from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category_id = models.IntegerField()
    subcategory_id = models.IntegerField()
    file_url = models.CharField(max_length=255)
    file_size = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'docs'

    def __str__(self):
        return self.title


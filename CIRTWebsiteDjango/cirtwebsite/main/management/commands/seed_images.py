from django.core.management.base import BaseCommand
from main.models import Images

class Command(BaseCommand):
    help = "Seed the Images table with demo rows"

    def handle(self, *args, **options):
        image_data = [
            # name,            author,            description,               file_type, file_size, file_url
            ("cirt-image-1",  "System Seeder",  "Promo shot for landing",   "image/jpeg", "245 KB", "images/cirt-image-1.jpg"),
            ("cirt-image-2",  "System Seeder",  "Hero banner background",   "image/jpeg", "310 KB", "images/cirt-image-2.jpg"),
            ("cirt-image-3",  "System Seeder",  "Thumbnail placeholder",    "image/png",  "512 KB", "images/cirt-image-3.png"),
        ]

        for name, author, description, file_type, file_size, file_url in image_data:
            obj, created = Images.objects.get_or_create(
                name=name,
                defaults={
                    "author": author,
                    "description": description,
                    "file_type": file_type,
                    "file_size": file_size,
                    "file_url": file_url,
                    # leave submitted_user=None so you can fill it later if needed
                },
            )
            action = "✔  created" if created else "↻  skipped (exists)"
            self.stdout.write(f"{action}: {name}")

        self.stdout.write(self.style.SUCCESS("Image seeding complete."))

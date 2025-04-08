from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Checking for existing users...")

        call_command('migrate')

        # Check if superuser exists, if not, create one
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(username='admin',email='parker@themalmgrens.com',password='adminpassword', first_name='admin', last_name='admin')
            print(f"Superuser created: {user.username}")
        else:
            print("Superuser already exists")

        # Check if other users exist, if not, create them
        users = [
            ('JohnDoe', 'johndoe@example.com', 'password123', '0', 'John', 'Doe'),
            ('maya', 'janedoe@example.com', 'maya', '1', 'Alice', 'Doe'),
            ('sayedali', 'bobdoe@example.com', 'password789', '0', 'Sayed', 'Ali'),
            ('abc', 'abc@example.com', 'abc', '0', 'Adam', 'Cobb', )
        ]

        for username, email, password, is_staff, first_name, last_name in users:
            if not User.objects.filter(username=username).exists():  # Check if the user exists
                user = User.objects.create_user(username=username, email=email, is_staff=is_staff, first_name=first_name, last_name=username)
                user.set_password(password)  # Hash the password before saving
                user.save()
                print(f"User {username} created")
            else:
                print(f"User {username} already exists")

        self.stdout.write(self.style.SUCCESS('Successfully created users'))

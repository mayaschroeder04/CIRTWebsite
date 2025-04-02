from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Checking for existing users...")

        call_command('migrate')

        # Check if superuser exists, if not, create one
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'parker@themalmgrens.com', 'adminpassword')
            print(f"Superuser created: {user.username}")
        else:
            print("Superuser already exists")

        # Check if other users exist, if not, create them
        users = [
            ('JohnDoe', 'johndoe@example.com', 'password123', '0'),
            ('AliceDoe', 'janedoe@example.com', 'password456', '1'),
            ('sayedali', 'bobdoe@example.com', 'password789', '0'),
            ('abc', 'abc@example.com', 'abc', '0')
        ]

        for username, email, password, is_staff in users:
            if not User.objects.filter(username=username).exists():  # Check if the user exists
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)  # Hash the password before saving
                user.save()
                print(f"User {username} created")
            else:
                print(f"User {username} already exists")

        self.stdout.write(self.style.SUCCESS('Successfully created users'))

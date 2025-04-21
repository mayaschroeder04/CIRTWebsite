from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management import call_command

User = get_user_model()  # dynamic and scalable for customuser


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Checking for existing users...")

        call_command('migrate')  # Ensure database is up to date

        # Check if superuser exists, if not, create one
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='parker@themalmgrens.com',
                password='adminpassword',
                first_name='admin',
                last_name='admin',
                role='admin'  # Assign 'admin' role
            )
            print(f"Superuser created: {user.username}")
        else:
            print("Superuser already exists")

        # Define users and their roles
        users = [
            ('JohnDoe', 'johndoe@example.com', 'password123', 'student', 'John', 'Doe'),
            ('maya', 'janedoe@example.com', 'maya', 'reviewer', 'Alice', 'Doe'),
            ('sayedali', 'bobdoe@example.com', 'password789', 'editor', 'Sayed', 'Ali'),
            ('abc', 'abc@example.com', 'abc', 'student', 'Adam', 'Cobb'),
        ]

        # Check if the "parker" user exists, if not, create it
        if not User.objects.filter(username='parker').exists():
            user = User.objects.create_user(username='parker', password='pass', is_active=False, role='student')
            print(f"User parker created")

        # Create other users if they do not exist
        for username, email, password, role, first_name, last_name in users:
            if not User.objects.filter(username=username).exists():  # Check if the user exists
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=role  # Assign the role to each user
                )
                user.set_password(password)  # Hash the password before saving
                user.save()
                print(f"User {username} created")
            else:
                print(f"User {username} already exists")

        self.stdout.write(self.style.SUCCESS('Successfully created users'))

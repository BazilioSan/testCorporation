import getpass

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        # email = input("Enter superuser email: ")
        email = "admin@admin.com"

        psw1 = getpass.getpass("Enter password: ")
        psw2 = getpass.getpass("Confirm password: ")

        while psw1 != psw2 or not psw1:
            print("Passwords didn't match or empty!")
            psw1 = getpass.getpass("Enter password: ")
            psw2 = getpass.getpass("Confirm password: ")

        user = User.objects.create(
            email=email,
            first_name="Admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(psw1)
        user.save()

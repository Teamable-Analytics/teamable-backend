from django.contrib.auth.models import User


class MyUser(User):
    pass


def __str__(self):
    return f"{self.first_name} {self.last_name}"

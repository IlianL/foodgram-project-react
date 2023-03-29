from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_superuser(self, email, password, username, **extra_fields):
        """Создаём суперпользователя и присваиваем ему роль админ."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.role = 'admin'
        user.created_by = 'admin'
        user.save()
        return user

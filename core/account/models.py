from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class UserManager(BaseUserManager):
    def create_user(self, email,**extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user_role, _ = Role.objects.get_or_create(role = 'user')
        user = self.model(email=email, role=user_role,**extra_fields)
        user.set_unusable_password()
        user.save()
        return user

    def create_company(self, email,**extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        company_role, _ = Role.objects.get_or_create(role = 'company')
        company = self.model(email=email, role=company_role,**extra_fields)
        company.set_unusable_password()
        company.save()
        return company

    def create_superuser(self, email,**extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email,**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """
    role = models.ForeignKey(Role,on_delete=models.PROTECT)
    email = models.EmailField(max_length=254, unique=True,db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT,editable=False)
    fullname = models.CharField(max_length=254)
    resume_file = models.FileField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email + "//" + self.fullname

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT,editable=False)
    name = models.CharField(max_length=100)
    logo = models.ImageField(null=True,blank=True)
    info = models.TextField()
    employee_number = models.IntegerField()


    def __str__(self):
        return self.user.email+"  " + self.user.role.role + " " + self.name

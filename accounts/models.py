from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid



class UserManager(BaseUserManager):
    def create_user(self, email, phone ,name,image,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.name=name
        user.phone=phone
        user.image=image
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password,name=None,phone=None,image=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            image=image
        )
        user.staff = True
        user.teacher = True
        user.admin = True
        user.student = False
        user.save(using=self._db)
        return user

    def create_teacher(self, email, phone ,name,image,password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
            image=image,
            password=password,
        )
        user.teacher = True
        user.student = False
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="user_images/",null=True,blank=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)
    token = models.CharField(max_length=500,null=True,blank=True) #This will store Temperary JWT Token
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False) # a admin user; non super-user
    student = models.BooleanField(default=True)
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name",'phone'] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_teacher(self):
        "True If User is a Teacher?"
        return self.teacher

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
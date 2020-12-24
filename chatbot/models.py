# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserProfileManager(BaseUserManager):
    """Class required by Django for managing our users from the management
    command.
    """

    def create_user(self, rno, name, password=None, sem=None, div=None):
        """Creates a new user with the given detials."""

        # Check that the user provided a roll number.
        if not rno:
            raise ValueError('Users must have a Roll number.')

        # Create a new user object.
        user = self.model(
            rno=rno,
            name=name,
            sem=sem,
            division=div,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, rno, name, password):
        """Creates and saves a new superuser with given detials."""

        # Create a new user with the function we created above.
        user = self.create_user(
            rno,
            name,
            password,
            None,
            None,
        )

        # Make this user an admin.
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """A user profile in our system."""

    rno = models.CharField(max_length=10, unique=True, blank=False, null=False)
    name = models.CharField(max_length=45, blank=True, null=True)
    sem = models.IntegerField(blank=True, null=True)
    division = models.CharField(max_length=1, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    workshop = models.BooleanField(default=True)
    sports = models.BooleanField(default=True)
    creative = models.BooleanField(default=True)
    cultural = models.BooleanField(default=True)
    placement = models.BooleanField(default=True)
    dance = models.BooleanField(default=True)
    drama = models.BooleanField(default=True)
    study = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ayear = models.CharField(max_length=2, null=True)
    batch = models.IntegerField(null=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'rno'

    class Meta:
        managed = True
        db_table = 'users'

    def get_full_name(self):
        """
        Required function so Django knows what to use as the users full name.
        """

        self.name

    def get_short_name(self):
        """
        Required function so Django knows what to use as the users short name.
        """

        self.name

    def __str__(self):
        """What to show when we output an object as a string."""

        return self.rno + ": " + self.name

class Individual(models.Model):
    rollno = models.CharField(max_length=10)
    notice = models.CharField(max_length=500)
    interest = models.CharField(max_length=15)
    date = models.DateField(auto_now_add=True)
    visited = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'individual'

class Information(models.Model):
    nid = models.AutoField(primary_key=True)
    notification = models.CharField(max_length=500)
    se_cmpn_a = models.BooleanField(default=False)
    se_cmpn_b = models.BooleanField(default=False)
    se_cmpn_c = models.BooleanField(default=False)
    te_cmpn_a = models.BooleanField(default=False)
    te_cmpn_b = models.BooleanField(default=False)
    te_cmpn_c = models.BooleanField(default=False)
    be_cmpn_a = models.BooleanField(default=False)
    be_cmpn_b = models.BooleanField(default=False)
    be_cmpn_c = models.BooleanField(default=False)
    ee1 = models.BooleanField(default=False)
    ee2 = models.BooleanField(default=False)
    ee3 = models.BooleanField(default=False)
    ee4 = models.BooleanField(default=False)
    ee5 = models.BooleanField(default=False)
    ee6 = models.BooleanField(default=False)
    interest = models.CharField(max_length=15)
    date = models.CharField(max_length=10)
    visited = models.IntegerField(default=0)
    # attachment = models.FileField(null=True)
    filepresent = models.BooleanField(default=False)
    filename = models.CharField(max_length=100,blank=True)

    class Meta:
        managed = True
        db_table = 'information'

class Support(models.Model):
    subject = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
    rno = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=0)
    c_date = models.CharField(max_length=10, blank=True)

    class Meta:
        managed = True
        db_table = 'support'
from django.db import models


# Creating model for userdata table.
class UserData(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=50, blank=False)
    user_password = models.CharField(max_length=150, blank=False)
    user_name = models.CharField(max_length=50, blank=False)
    user_last_name = models.CharField(max_length=50, blank=False)
    user_occupation_name = models.CharField(max_length=80, blank=False)
    user_location_name = models.CharField(max_length=150, blank=False)
    signup_date = models.CharField(max_length=10, blank=False)  # yyyy-mm-dd
    record_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.CharField(max_length=50, blank=True, default="P")

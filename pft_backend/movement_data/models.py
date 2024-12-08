from django.db import models

# Creating model data for movement records.
class MovementData(models.Model):
    mov_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('login.UserData',related_name='user_ids2', on_delete=models.CASCADE)
    mov_catg_id = models.ForeignKey('mov_category.MovCategory', related_name='mov_catg_ids2', on_delete=models.CASCADE)
    mov_period = models.CharField(max_length=7, blank=False) #2025-01
    mov_value = models.CharField(max_length=150, blank=False)
    mov_date = models.CharField(max_length=10, blank=False) #yyyy-MM-dd
    mov_description = models.CharField(max_length=200, blank=True)
    period_is_open = models.CharField(max_length=1, blank=False, default="Y")
    record_date = models.DateTimeField(auto_now_add=True)


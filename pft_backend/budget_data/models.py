from django.db import models

# Creating model data for budget records.
class BudgetData(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('login.UserData',related_name='user_ids', on_delete=models.CASCADE)
    mov_catg_id = models.ForeignKey('mov_category.MovCategory', related_name='mov_catg_ids', on_delete=models.CASCADE)
    budget_period = models.CharField(max_length=7, blank=False)
    budget_value = models.CharField(max_length=150, blank=False)
    budget_description = models.CharField(max_length=200, blank=True)
    period_status = models.CharField(max_length=2, blank=False, default="No")
    record_date = models.DateTimeField(auto_now_add=True)


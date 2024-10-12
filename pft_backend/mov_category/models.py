from django.db import models

# Creating models for movement category table.
class MovCategory(models.Model):
    mov_catg_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=30, blank=False) #personal_finances or trips
    category_name = models.CharField(max_length=30, blank=False)
    category_description = models.CharField(max_length=80, blank=True)
    record_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.CharField(max_length=50, blank=True, default="P")

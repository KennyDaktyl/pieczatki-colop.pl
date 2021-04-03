from django.contrib import admin
from .models import Pages
# Register your models here.


@admin.register(Pages)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Pages._meta.fields]
    list_filter = (
        # 'name',
        # 'worker_position',
    )
    # search_fields = (
    #     'last_name',
    #     'username',
    # )

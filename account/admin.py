from django.contrib import admin
from account.models import Profile, Address
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    list_filter = (
        'company',
        # 'worker_position',
    )
    search_fields = (
        'last_name',
        'username',
        'nip_number',
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Address._meta.fields]
    list_filter = (
        # 'workplace',
        # 'worker_position',
    )
    search_fields = ('user_id', )

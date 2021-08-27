from django.contrib import admin

# Register your models here.
from account.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_org')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = ()
    list_filter = ()
    filter_horizontal = ()
    

admin.site.register(Account, AccountAdmin)
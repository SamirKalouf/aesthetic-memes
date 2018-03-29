from django.contrib import admin

from .models import Profile
# Register your models here

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def get_user_first_name(self,obj):
        return obj.user.first_name
    get_user_first_name.short_description = 'First Name'
    def get_user_last_name(self,obj):
        return obj.user.last_name
    get_user_last_name.short_description = 'Last Name'
    def get_user_last_login(self,obj):
        return obj.user.last_login
    get_user_last_login.short_description = 'Last Login'

    list_select_related = True
    list_display = ('user','get_user_first_name', 'get_user_last_name', 'get_user_last_login')
    list_filter =(
        'user__last_login',)
    search_fields = ('user__username','user__first_name', 'user__last_name')

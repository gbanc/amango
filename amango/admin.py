from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm

# Run admin.site.register() for each model we wish to register
# with the REAL django admin!
from profiles.admin import ProfileAdmin
from profiles.models import Profile


class UserAdmin(AdminSite):
    login_form = AuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

user_admin_site = UserAdmin(name='usersadmin')
user_admin_site.register(Profile, ProfileAdmin)
# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users

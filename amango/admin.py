from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from profiles.models import Profile
from amango.forms import UserAdminAuthenticationForm

class UserAdmin(AdminSite):
    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

user_admin_site = UserAdmin(name='usersadmin')
user_admin_site.register(Profile)
# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users

# Run admin.site.register() for each model we wish to register
# with the REAL django admin!
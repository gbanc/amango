from django.contrib import admin

from profiles.forms import AddProfileForm
from users.models import User

from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    # fields = ('seller_id', 'mws_auth_token', 'marketplace_id')
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(user_id=request.user)
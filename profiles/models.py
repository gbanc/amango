from django.db import models
from users.models import User
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_id = models.TextField(null=True)
    mws_auth_token = models.TextField(null=True)
    marketplace_id = models.TextField(null=True, default='ATVPDKIKX0DER', help_text='Defaults to US marketplace ID')

    def __str__(self):
        return '%s' % (self.seller_id)
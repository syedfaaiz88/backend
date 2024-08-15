from django.contrib import admin
from .models import User

# Register the User and Gender models with the custom UserAdmin and GenderAdmin
admin.site.register(User)

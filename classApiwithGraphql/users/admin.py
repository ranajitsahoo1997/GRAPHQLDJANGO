from django.contrib import admin
from .models import ExtendUser,Post
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = ExtendUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('link',)}),
    )

admin.site.register(ExtendUser)
admin.site.register(Post)



app = apps.get_app_config('graphql_auth')

for model_name,model in app.models.items():
    admin.site.register(model)

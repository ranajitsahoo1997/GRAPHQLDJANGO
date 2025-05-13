from django.contrib import admin
from.models import AuthUser
from django.contrib.auth.admin import UserAdmin 
from django.apps import apps
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = AuthUser
#     # fieldsets= UserAdmin.fieldsets + (
#     #     (None, {'fields': ('email',)}),
#     # )
admin.site.register(AuthUser)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)

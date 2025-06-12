from django.contrib import admin
from .models import User
from django.utils.safestring import mark_safe


class UsersAdministrate(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "date_birth",
        "gender_choice",
        "get_object_image",
    )
    list_display_links = ("username",)
    search_fields = ("username", "email")
    readonly_fields = ("get_object_image",)

    def get_object_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")


admin.site.register(User, UsersAdministrate)

admin.site.site_title = "AeraPolisi Administration"
admin.site.site_header = "AeraPolisi Administration"

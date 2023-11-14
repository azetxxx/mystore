from django.contrib import admin

from users.models import EmailVerification, User

# Register your models here.

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', 'user')

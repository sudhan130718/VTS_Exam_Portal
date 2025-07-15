from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from django.apps import apps

from .models import User, Trainer
from .models import Trainee, Course



User = apps.get_model(settings.AUTH_USER_MODEL)
# ------------------------------
# Custom User Admin
# ------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'mobile', 'profile_image')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)


# ------------------------------
# Trainer Form for Admin
# ------------------------------
class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrainerForm, self).__init__(*args, **kwargs)

        # Get all users who are already assigned to a Trainer
        assigned_users = Trainer.objects.values_list('user_id', flat=True)

        # If editing, include current user to avoid exclusion
        if self.instance and self.instance.pk:
            self.fields['user'].queryset = User.objects.exclude(
                id__in=assigned_users
            ).union(User.objects.filter(id=self.instance.user_id))
        else:
            self.fields['user'].queryset = User.objects.exclude(id__in=assigned_users)


# ------------------------------
# Trainer Admin
# ------------------------------
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    form = TrainerForm

    list_display = (
        'full_name', 'user_email', 'get_expertise_display',
        'get_technical_languages', 'city', 'is_active'
    )

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = 'Name'

    def user_email(self, obj):
        return obj.user.email

    def get_expertise_display(self, obj):
        return obj.get_expertise_area_display()

    def get_technical_languages(self, obj):
        return ", ".join(obj.get_technical_languages_list())


admin.site.register(Trainee)
admin.site.register(Course)


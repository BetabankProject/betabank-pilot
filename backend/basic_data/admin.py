from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile
from .models import SkillFamily
from .models import Skill
from .models import InitialCapital
from .models import Request
from .models import Offer


admin.site.register(Profile)
admin.site.register(SkillFamily)
admin.site.register(Skill)
admin.site.register(InitialCapital)
admin.site.register(Request)
admin.site.register(Offer)


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    # verbose_name_plural = 'employee'


# Define a new User admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
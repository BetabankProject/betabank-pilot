from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import SkillFamily
from .models import Skill
from .models import InitialCapital
from .models import Request


admin.site.register(Profile)
admin.site.register(SkillFamily)
admin.site.register(Skill)
admin.site.register(InitialCapital)
admin.site.register(Request)
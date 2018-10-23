from django.contrib import admin
from ui_web.models import MeetingInfo, RoleTakers, Speakers, Members

# Register your models here.


class SpeakersInline(admin.TabularInline):
    model = Speakers


class RoleTakersAdmin(admin.ModelAdmin):
    inlines = [SpeakersInline]


admin.site.register([MeetingInfo, Members])
admin.site.register(RoleTakers, RoleTakersAdmin)
from django.contrib import admin
from ui_web.models import MeetingInfo, RoleTakers, Speakers, Members

# Register your models here.


class SpeakersInline(admin.TabularInline):
    model = Speakers


class RoleTakersAdmin(admin.ModelAdmin):
    inlines = [SpeakersInline]


class MeetingInfoAdmin(admin.ModelAdmin):

    filter_horizontal = ("attendance",)


class MembersAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Members, MembersAdmin)
admin.site.register(MeetingInfo, MeetingInfoAdmin)
admin.site.register(RoleTakers, RoleTakersAdmin)

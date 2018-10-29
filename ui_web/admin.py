from django.contrib import admin
from ui_web.models import MeetingInfo, Speakers, Members

# Register your models here.


class SpeakersInline(admin.TabularInline):
    model = Speakers


class RoleTakersAdmin(admin.ModelAdmin):
    inlines = [SpeakersInline]


class MeetingInfoAdmin(admin.ModelAdmin):

    filter_horizontal = ("attendance", "individual_evaluator")
    # raw_id_fields = ('publisher',)


class MembersAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Members, MembersAdmin)
admin.site.register(MeetingInfo, MeetingInfoAdmin)
# admin.site.register(RoleTakers, RoleTakersAdmin)

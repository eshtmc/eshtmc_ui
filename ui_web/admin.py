from django.contrib import admin
from ui_web.models import MeetingInfo, Speakers, Members
from django.forms.models import model_to_dict
# from django.contrib import
# Register your models here.


class SpeakersInline(admin.TabularInline):
    model = Speakers


class MeetingInfoAdmin(admin.ModelAdmin):
    search_fields = ['theme', 'count']
    ordering = ['count']
    list_display = ('date', 'count', 'theme')
    filter_horizontal = ("attendance", "individual_evaluator")
    date_hierarchy = 'date'
    list_per_page = 30

    inlines = [SpeakersInline]

    def save_model(self, request, obj, form, change):
        for key, value in model_to_dict(obj).items():
            if value is None:
                self.message_user(
                    request, "{0} will use the default value 'eshtmc'".format(key))
                setattr(obj, key+"_id", 1)
                # set the default value 1, it will be set eshtmc info
        super(MeetingInfoAdmin, self).save_model(request, obj, form, change)

    actions = ['create_new_info']

    def create_new_info(self, request, queryset):

        for obj in queryset:
            for key, value in vars(obj).items():
                if key.split("_")[-1] == 'id':
                    value = Members.objects.filter(
                        id=value).values("name")[0].get("name")

                print(key, value)
        self.message_user(request, "changed in https://eshtmc.github.io/")
        pass

    create_new_info.short_description = "create_new_info on the github page"


class MembersAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_display = ('name', 'email', 'rank', 'date', 'on_activate')
    date_hierarchy = 'date'
    list_editable = ('email', 'rank')
    list_filter = ('rank', 'date', 'on_activate')
    list_per_page = 30


admin.site.register(Members, MembersAdmin)
admin.site.register(MeetingInfo, MeetingInfoAdmin)


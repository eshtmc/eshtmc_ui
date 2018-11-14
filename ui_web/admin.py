from django.contrib import admin
from ui_web.models import MeetingInfo, Speakers, Members
from django.forms.models import model_to_dict
from .tool.eshtmc_data import github_page
# from django.contrib import
# Register your models here.


class SpeakersInline(admin.TabularInline):
    model = Speakers


class MeetingInfoAdmin(admin.ModelAdmin):
    search_fields = ['theme', 'count']
    ordering = ['count']
    list_display = ('date', 'count', 'theme')
    filter_horizontal = ("attendance",
                         "individual_evaluator",
                         "table_topic_speaker")
    date_hierarchy = 'date'
    list_per_page = 30

    inlines = [SpeakersInline]

    def save_model(self, request, obj, form, change):
        for key, value in model_to_dict(obj).items():
            if key != "id" and value is None:
                self.message_user(
                    request, "{0} will use the default value 'eshtmc'".format(key))
                setattr(obj, key+"_id", Members.objects.get(name="eshtmc").id)
                # set the default value eshtmc.id, it will be set eshtmc info
        super(MeetingInfoAdmin, self).save_model(request, obj, form, change)

    actions = ['create_new_info']

    def create_new_info(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request, "nothing change, you can only choose one info")
        else:
            meeting_info = {}
            for obj in queryset:
                for key, value in vars(obj).items():
                    if key.find("_id") != -1:
                        value = Members.objects.get(id=value).name
                    if key != "_state":
                        meeting_info[key.split("_id")[0]] = value

                meeting_info["attendance"] = ",".join(
                    [str(x) for x in model_to_dict(obj)["attendance"]])
                meeting_info["table_topic_speaker"] = ",".join(
                    [str(x) for x in
                     model_to_dict(obj)["table_topic_speaker"]])
                meeting_info["individual_evaluator"] = ",".join(
                    [str(x) for x in
                     model_to_dict(obj)["individual_evaluator"]])
                meeting_info['date'] = ".".join(
                    str(meeting_info['date']).split('-'))

                #  get the Speakers form the database
                speaker_list = list()
                for speaker in Speakers.objects.filter(meeting_info_id=obj.id):
                    speaker_dict = dict()
                    speaker_dict["project_rank"] = speaker.project_rank
                    speaker_dict["people_name"] = str(speaker.speaker_name)
                    speaker_dict["project_name"] = speaker.project_title
                    speaker_list.append(speaker_dict)
                meeting_info['prepared_speakers'] = speaker_list
                github_page(meeting_info)
            self.message_user(request, "changed in https://eshtmc.github.io/")

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


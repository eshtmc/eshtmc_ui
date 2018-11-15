from django.shortcuts import render
from django.db.models import Count
from collections import Counter
from .models import MeetingInfo, Members
from django.http import HttpResponse
from django.template import loader
from pyecharts import Pie, WordCloud


REMOTE_HOST = 'https://pyecharts.github.io/assets/js'
# Create your views here.


def index(request):
    return render(request, 'index.html')


def show_data(request):
    template = loader.get_template('meetings/show_data.html')


    # attr = [u"members", "non-members"]
    # value = [Members.objects.filter(on_activate=True).count(),
    #          Members.objects.filter(on_activate=False).count()]
    # pie = Pie(u"Members and non-members")
    # pie.add("Count", attr, value)
    # context = dict(
    #     pie=pie.render_embed(),
    #     host=REMOTE_HOST,
    #     script_list=pie.get_js_dependencies()
    # )


    names = Members.objects.values_list('id')
    print(names)
    meeting_attendace = Counter(MeetingInfo.objects.values_list('attendance'))
    attr_attendace = [Members.objects.get(id=key[0]).name
            for key, _ in meeting_attendace.items()]
    value_attendace = [value for value in meeting_attendace.values()]
    print(11,attr_attendace)
    print(22,value_attendace)
    wordcloud = WordCloud()
    wordcloud.add("attendace", attr_attendace, value_attendace)
    wordcloud.show_config()
    # wordcloud.render()
    context = dict(
        pie=wordcloud.render_embed(),
        host=REMOTE_HOST,
        script_list=wordcloud.get_js_dependencies()
    )

    return HttpResponse(template.render(context, request))


def members(request):
    members = Members.objects.values_list()
    return render(request, 'members/members.html', {'members': members})
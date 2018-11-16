from django.shortcuts import render
from django.db.models import Count
from collections import Counter, OrderedDict
from .models import MeetingInfo, Members
from django.http import HttpResponse
from django.template import loader
from pyecharts import Pie, WordCloud, Bar, Line, EffectScatter


REMOTE_HOST = 'https://pyecharts.github.io/assets/js'
# Create your views here.


def index(request):
    return render(request, 'index.html')


def show_data(request):
    template = loader.get_template('meetings/show_data.html')

    attr = [u"members", "non-members"]
    value = [Members.objects.filter(on_activate=True).count(),
             Members.objects.filter(on_activate=False).count()]
    pie = Pie(u"Members and non-members")
    pie.add("Count", attr, value)

    meeting_attendace = Counter(MeetingInfo.objects.values_list('attendance'))
    attr_attendace = OrderedDict()
    attr_attendace.update({Members.objects.get(id=key[0]).name: value
                           for key, value in meeting_attendace.items()})

    wordcloud = WordCloud()
    wordcloud.add("attendace", list(attr_attendace.keys()),
                  list(attr_attendace.values()))

    bar = Bar("attendaces")
    bar.add("attendaces", list(attr_attendace.keys()),
            list(attr_attendace.values()), xaxis_interval=0, xaxis_rotate=-90)

    meeting_info = MeetingInfo.objects.values_list(
        'date', 'count', 'theme').annotate(Count('attendance'))
    meeting_info_dict = OrderedDict()
    for m in meeting_info:
        meeting_info_dict[str(m[0])+'#'+str(m[1])+str(m[2])] = int(m[3])
        print(str(m[0])+'_'+str(m[1])+str(m[2]), m[3])

    line = Line("Meeting attendance number")
    line.add("ESHTMC", list(meeting_info_dict.keys()),
             list(meeting_info_dict.values()), mark_point=["average"],
             xaxis_interval=0, xaxis_rotate=-45)

    context = dict(
        host=REMOTE_HOST,
        pie=pie.render_embed(),
        pie_script_list=pie.get_js_dependencies(),
        wordcloud=wordcloud.render_embed(),
        wordcloud_script_list=wordcloud.get_js_dependencies(),
        bar=bar.render_embed(),
        bar_script_list=bar.get_js_dependencies(),
        line=line.render_embed(),
        line_script_list=line.get_js_dependencies(),
    )

    return HttpResponse(template.render(context, request))


def members(request):
    members = Members.objects.values_list()
    return render(request, 'members/members.html', {'members': members})

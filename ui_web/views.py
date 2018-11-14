from django.shortcuts import render
from .models import MeetingInfo, Members
# Create your views here.


def index(request):
    return render(request, 'index.html')


def show_data(request):
    members = Members.objects.values_list()
    return render(request, 'meetings/show_data.html', {'members': members})


def members(request):
    members = Members.objects.values_list()
    return render(request, 'members/members.html', {'members': members})
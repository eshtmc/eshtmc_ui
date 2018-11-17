from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    path('data', views.show_data),
    path('members', views.members),
    path('meetings', views.meetings)

]

urlpatterns += staticfiles_urlpatterns()
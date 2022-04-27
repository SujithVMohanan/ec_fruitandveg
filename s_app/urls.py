from django.urls import path
from . import views

app_name = 's_app'
urlpatterns = [
    path('',views.search_result, name='searchR'),

]
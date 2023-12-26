from django.urls import path
from . import views

urlpatterns = [
    path('show_data/', views.show_data),  # '/show_data' 경로를 'show_data' 뷰에 연결합니다.
]

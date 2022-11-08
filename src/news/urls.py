from django.contrib import admin
from django.urls import path, include
from src.news.views import BaseView, PostsList, PostDetail, PostCreate, PostEditView, PostDeleteView, add_subscribe

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),

]

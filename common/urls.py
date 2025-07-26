from django.urls import path

from common.views import HomeView, contacts_page_view, help_page_view, cookies_page_view

urlpatterns =[
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts_page_view, name='contacts'),
    path('help/', help_page_view, name='help'),

    path('cookies/', cookies_page_view, name='cookies'),
]
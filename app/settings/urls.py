from currency import views as currency_views

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', currency_views.index),
    path('hello-world/', currency_views.hello_world),
    path('contacts/list/', currency_views.contacts_list),
    path('rate/list/', currency_views.rate_list),
    path('source/list/', currency_views.source_list),
    path('source/create/', currency_views.source_create),
    path('source/update/<int:pk>/', currency_views.source_update),
    path('source/delete/<int:pk>/', currency_views.source_delete),
]

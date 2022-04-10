from currency import views as currency_views

from django.urls import path

app_name = 'currency'

urlpatterns = [
    # path('example/', currency_views.ExampleView.as_view(), name='example'),
    path('contactus/list/', currency_views.ContactUsList.as_view(), name='contactus_list'),
    path('contactus/create/', currency_views.ContactUsCreate.as_view(), name='contactus_create'),
    path('rate/list/', currency_views.RateList.as_view(), name='rate_list'),
    path('rate/update/<int:pk>/', currency_views.RateUpdate.as_view(), name='rate_update'),
    path('source/list/', currency_views.SourceList.as_view(), name='source_list'),
    path('source/create/', currency_views.SourceCreate.as_view(), name='source_create'),
    path('source/update/<int:pk>/', currency_views.SourceUpdate.as_view(), name='source_update'),
    path('source/delete/<int:pk>/', currency_views.SourceDelete.as_view(), name='source_delete'),
    path('source/detail/<int:pk>/', currency_views.SourceDetail.as_view(), name='source_detail'),
]

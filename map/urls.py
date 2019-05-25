from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('comment/', views.add_comment, name='addcomment'),
    path('location/', views.add_location, name='addlocation'),
    path('delete/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('reset/', views.reset, name='reset'),
    path('filtered/', views.filtered, name='filtered'),
    path('home/', views.home, name='home'),
    path('contact/', views.contactadmin, name='contact'),
    path('contact_page/', views.contactListPage, name='contact_page'),
    path('deletemsg/', views.deletemsg, name='deletemsg'),
]

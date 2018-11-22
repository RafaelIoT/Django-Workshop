from django.conf.urls       import url
from django.contrib         import admin
from django.contrib.auth    import views as auth_views
from django.urls            import path
from .                      import views


urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('home/', views.home, name='home'),
    path('mean/', views.get_mean, name='get_mean'),
    path('new_grade/', views.add_grade, name='add_grade'),
]

from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('home/', views.home, name="home"),
	path('logout/',views.logout_view,name='logout'),
 	path('about/',views.about,name='about'),
 	path('FILE/',views.FILE,name='FILE'),
  path('homebefore/', views.homebefore, name="homebefore"),
   


	
    ]

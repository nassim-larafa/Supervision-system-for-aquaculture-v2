from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('services/',views.services),
    path('projects/',views.projets),
    path('contacts/',views.contact),
    path('signup/', include('users.urls')),
    path('connect/', include('users.urls')),
    path('login/', include('users.urls')),
]

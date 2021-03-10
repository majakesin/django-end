"""djangoEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import settings
from movie.routerMovie import routerMovie
from movie.views import LikeDislikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('jwtAuthentication.urls')),
    path('api/movies/', include(routerMovie.urls)),
    path('api/movies/like/', LikeDislikeView.as_view(), name="like"),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

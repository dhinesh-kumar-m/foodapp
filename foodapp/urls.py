"""foodapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="restaurant:restaurant_list", permanent=False
        ),
    ),
    path("admin/", admin.site.urls),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("restaurants/", include("restaurant.urls")),
    path("bookmarks/", include("bookmark.urls")),
    path("spotlights/", include("spotlight.urls")),
    path("visited/", include("visited.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

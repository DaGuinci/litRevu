"""
URL configuration for litRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LogoutView
    )
from django.urls import include, path
from review import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('posts/', views.user_posts, name='user_posts'),
    path('login/', views.log_user_in, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_page, name='signup'),
    path('add-review/', views.add_review, name='add_review'),
    path(
        'add-review-to/<int:ticket_id>',
        views.add_review_to,
        name='add_review_to'
        ),
    path('edit-review/<int:id>', views.edit_review, name='edit_review'),
    path('delete-review/<int:id>', views.delete_review, name='delete_review'),
    path('add-ticket/', views.add_ticket, name='add_ticket'),
    path('edit-ticket/<int:id>', views.edit_ticket, name='edit_ticket'),
    path('delete-ticket/<int:id>', views.delete_ticket, name='delete_ticket'),
    path('subscribes/', views.subscribes, name='subscribes'),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

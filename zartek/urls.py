from django.contrib import admin
from django.urls import path,include
from postapi import views
from postapi.router import router
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('post/<int:pk>/like',views.LikePost.as_view(),name='like-post'),
    path('post/<int:pk>/dislike',views.DislikePost.as_view(),name='dislike-post'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

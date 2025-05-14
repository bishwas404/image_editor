from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.upload_view,name='upload'),
    path('crop-image/', views.crop_image_view, name='crop-image'),
    path('background-image/', views.remove_background_view, name='background-remove'),
    path('result/<int:image_id>/<uuid:unique_id>/', views.result_view, name='result'),
    path('download/<int:image_id>/<uuid:unique_id>/', views.download_image, name='download_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

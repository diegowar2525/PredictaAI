from django.urls import path
from .views import camera_test_view, detect_from_image

app_name = "barcode_engine"  # Agrega esta línea

urlpatterns = [
    path("test/", camera_test_view, name="barcode_test"),
    path("detect/", detect_from_image, name="barcode_detect"),
]

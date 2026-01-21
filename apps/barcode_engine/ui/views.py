from django.shortcuts import render
from django.http import JsonResponse
import base64
import cv2
import numpy as np

from apps.barcode_engine.services.barcode_service import process_frame


def camera_test_view(request):
    return render(request, "barcode_engine/camera_test.html")


def detect_from_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    image_data = request.POST.get("image")

    if not image_data:
        return JsonResponse({"error": "No image received"}, status=400)

    header, encoded = image_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)

    np_arr = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = process_frame(image)

    return JsonResponse({"results": results})

import cv2
from pyzbar.pyzbar import decode

def detect_barcodes(frame, flip=True):
    if flip:
        frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)

    detections = []

    for barcode in barcodes:
        detections.append({
            "codigo": barcode.data.decode("utf-8"),
            "tipo": barcode.type,
            "rect": barcode.rect
        })

    return frame, detections

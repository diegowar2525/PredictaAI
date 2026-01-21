from apps.barcode_engine.services.detector import detect_barcodes
from apps.barcode_engine.storage.firebase_store import save_barcode_record
import datetime  # Agrega esta importación para el timestamp

def process_frame(image):
    """
    Procesa una imagen/frame:
    - detecta códigos de barras
    - guarda el resultado
    - devuelve los datos detectados
    """

    frame, detections = detect_barcodes(image)  # Desempaqueta la tupla

    records = []

    for barcode in detections:  # Itera sobre la lista de detecciones
        record = {
            "code": barcode["codigo"],  # Cambia a la clave correcta
            "type": barcode["tipo"],    # Cambia a la clave correcta
            "timestamp": datetime.datetime.now().isoformat(),  # Agrega timestamp actual
        }

        save_barcode_record(record)
        records.append(record)

    return records




























# from apps.barcode_engine.services.detector import detect_barcodes
# from apps.barcode_engine.storage.firebase_store import save_barcode_record


# def process_frame(image):
#     """
#     Procesa una imagen/frame:
#     - detecta códigos de barras
#     - guarda el resultado
#     - devuelve los datos detectados
#     """

#     results = detect_barcodes(image)

#     records = []

#     for barcode in results:
#         record = {
#             "code": barcode["code"],
#             "type": barcode["type"],
#             "timestamp": barcode["timestamp"],
#         }

#         save_barcode_record(record)
#         records.append(record)

#     return records

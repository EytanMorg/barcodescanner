import cv2
from pyzbar import pyzbar
import pylibdmtx
import sys
import pyperclip
import time

def set_focus(camera, value):
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    camera.set(cv2.CAP_PROP_FOCUS, value)

def scan_barcode():
    front_camera_index = 0
    cap = cv2.VideoCapture(front_camera_index)

    focus_value = 0.0
    set_focus(cap, focus_value)

    last_focus_change_time = time.time()

    while True:
        ret, frame = cap.read()
        barcodes = pyzbar.decode(frame)
        
        for barcode in barcodes:
            (x, y, w, h) = barcode.sqr()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcode_data = barcode.data.decode('utf-8')
            text = f"{barcode_data})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            pyperclip.copy(barcode_data)
            print(f"Barcode data: {barcode_data}")
            sys.exit(0)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Barcode Scanner', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        # Check if it's time to change the focus
        if time.time() - last_focus_change_time > 3:
            focus_value = (focus_value + 0.5) % 1.0
            set_focus(cap, focus_value)
            last_focus_change_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcode()

    # https://www.myinstants.com/nl/instant/tu-tu-tu-du-max-verstappen-18834/
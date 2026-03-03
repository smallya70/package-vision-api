import cv2
import requests
from ultralytics import YOLO
import time

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/api/v1/route-package"
# Update this path to wherever you saved your trained YOLO model!
MODEL_PATH = "best.pt" 

print("Loading YOLO model...")
model = YOLO(MODEL_PATH)

# Initialize Webcam (0 is usually your laptop's built-in camera)
cap = cv2.VideoCapture(0)
print("Webcam activated. Press 'q' on the video window to quit.")

# Timer to prevent spamming the API 30 times a second
last_api_call = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame, conf=0.15, verbose=False)
    # 1. Run YOLO on the live webcam frame
    
    # 2. Analyze what the AI sees
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract the AI's prediction
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]

            # Draw a visual bounding box on your screen
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 3. Send to FastAPI (Simulating a conveyor belt gap of 2 seconds)
            if time.time() - last_api_call > 2.0:
                payload = {
                    "material_id": f"LIVE-SCAN-{int(time.time())}", 
                    "class_name": class_name,
                    "confidence": confidence
                }
                
                try:
                    # POST the prediction to your enterprise backend
                    response = requests.post(API_URL, json=payload)
                    decision = response.json().get("recommended_erp_action", "Error")
                    
                    print(f"📦 Scanned: {class_name} ({confidence:.2f}) | ERP Action: {decision}")
                    
                except requests.exceptions.ConnectionError:
                    print("⚠️ Could not connect to FastAPI. Is the server running?")
                
                last_api_call = time.time()

    # Show the live video feed
    cv2.imshow("Inbound Quality Gate", frame)

    # Press 'q' to shut down the camera
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
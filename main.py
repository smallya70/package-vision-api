from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# Initialize the API
app = FastAPI(
    title="Inbound Quality & Routing Agent",
    description="Microservice connecting YOLO vision output to material management routing."
)

class VisionPayload(BaseModel):
    material_id: str
    class_name: str
    confidence: float

@app.post("/api/v1/route-package")
async def evaluate_package(payload: VisionPayload):
    confidence_threshold = 0.20

    if payload.confidence < confidence_threshold:
        return _build_response("MANUAL_REVIEW", "AI confidence too low.", "Route to Exception Handling Desk")

    if payload.class_name == "DamagePackage":
        action = "Post to Blocked Stock / Trigger Vendor Return"
        reason = f"Severe damage detected (Confidence: {payload.confidence:.2f})"
        return _build_response("QUARANTINE", reason, action)

    elif payload.class_name == "Open box":
        action = "Route to QA Work Center"
        reason = f"Package is open, verify contents (Confidence: {payload.confidence:.2f})"
        return _build_response("INSPECTION", reason, action)

    elif payload.class_name == "Box":
        action = "Post Goods Receipt to Unrestricted-Use"
        reason = f"Package intact (Confidence: {payload.confidence:.2f})"
        return _build_response("CLEARED", reason, action)
    
    else:
        return _build_response("ERROR", "Unknown defect class detected.", "N/A")

def _build_response(status: str, reason: str, erp_action: str):
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "routing_status": status,
        "reason_code": reason,
        "recommended_erp_action": erp_action
    }
# Inbound Quality & Routing Agent (Edge AI)

An automated, edge-deployed computer vision microservice designed to streamline inbound goods receipt processes. This system uses a custom-trained YOLOv26 model to inspect packages and a FastAPI backend to route materials based on enterprise supply chain logic.

## 🏗️ Architecture
1. **Vision Layer (Edge):** Python/OpenCV script capturing live video and running YOLO inference.
2. **Decision Engine (API):** A FastAPI microservice that ingests AI predictions and outputs JSON routing directives.

## ⚙️ Enterprise Business Logic
The API translates visual data into standard material management routing decisions:
* **Box (Intact):** Cleared for standard Goods Receipt (Unrestricted-Use stock).
* **Open box:** Diverted to QA Work Center for manual inspection.
* **DamagePackage:** Flagged for Quarantine (Post to Blocked Stock / Vendor Return).
* **Failsafe (<20% Confidence):** Routed to **Exception Handling Desk** to prevent automated errors.

## 🛠️ Tech Stack
* **AI/Vision:** YOLOv26, OpenCV
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Environment:** Python venv
* ## Project Preview, paste this line:
![API Response Preview](api_response.png)

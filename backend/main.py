from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pipeline import generate_response
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the audios directory exists and serve static files
os.makedirs("audios", exist_ok=True)
app.mount("/audios", StaticFiles(directory="audios"), name="audios")

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()

        if not user_message:
            return {"text": "❗ Please enter a message."}

        response = generate_response(user_message)

        # If audio was generated, return its public URL path
        if "audio" in response:
            filename = os.path.basename(response["audio"])
            response["audio"] = f"/audios/{filename}"

        return response

    except Exception as e:
        print("❌ Error:", str(e))
        return {"text": f"Internal server error: {str(e)}"}

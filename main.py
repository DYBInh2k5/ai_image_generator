from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import requests
import urllib.parse

app = FastAPI(title="AI Image Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_image(req: PromptRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
        
    try:
        # We use a reliable free open text-to-image API.
        encoded_prompt = urllib.parse.quote(req.prompt)
        url = f"https://api.airforce/imagine?prompt={encoded_prompt}"
        
        print(f"Generating image for prompt: '{req.prompt}'")
        response = requests.get(url, timeout=45)
        response.raise_for_status()
        print("Image generated successfully!")
        
        return Response(content=response.content, media_type="image/jpeg", headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

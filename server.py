from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionPipeline
import io

app = FastAPI(title="Local AI Image Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# -----------------
# INITIALIZE MODEL
# -----------------
print("Loading Stable Diffusion Model (This might take a while on first run to download ~4GB)...")
model_id = "runwayml/stable-diffusion-v1-5" # A robust, standard base model

# Check if CUDA (Nvidia GPU) is available, otherwise fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using compute device: {device.upper()}")

# Load pipeline. If GPU, use float16 to save huge VRAM.
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    model_id, 
    torch_dtype=dtype,
    safety_checker=None # Disabled to prevent memory overhead and false positives
)

pipe = pipe.to(device)

# Optional memory optimization
if device == "cuda":
    pipe.enable_attention_slicing()

print("Model successfully loaded into memory!")


@app.post("/generate")
async def generate_image(req: PromptRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
        
    try:
        print(f"Generating image locally for prompt: '{req.prompt}'")
        
        # Run local inference
        # num_inference_steps=20 for faster generation, guidance_scale=7.5 is standard
        image = pipe(
            req.prompt, 
            num_inference_steps=20, 
            guidance_scale=7.5,
            height=512, # 512x512 is standard SD v1.5 size and fits in VRAM better
            width=512
        ).images[0]
        
        print("Image generated successfully!")
        
        # Convert image to byte stream
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=90)
        img_byte_arr.seek(0)
        
        return Response(content=img_byte_arr.getvalue(), media_type="image/jpeg", headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Start on custom port to avoid conflict with old instances
    uvicorn.run(app, host="127.0.0.1", port=8001)

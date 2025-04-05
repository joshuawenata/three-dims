from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import subprocess
import os
import uuid
from pathlib import Path
from typing import Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_gif(data: Dict[str, Any] = Body(...)):
    try:
        prompt = data.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        gen_id = str(uuid.uuid4())
        output_dir = Path(f"outputs/{gen_id}")
        output_dir.mkdir(parents=True, exist_ok=True)

        ai_script_path = os.path.join(os.path.dirname(__file__), "..", "ai", "main.py")
        command = [
            "python",
            ai_script_path,
            "--prompt",
            prompt,
            "--output_dir",
            str(output_dir)
        ]
        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Output dari ai/main.py:\n{process.stdout}")
        print(f"Error dari ai/main.py:\n{process.stderr}")

        return {
            "gif_url": f"http://localhost:8000/download/{gen_id}",
            "id": gen_id,
        }

    except subprocess.CalledProcessError as e:
        print(f"Error subprocess: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    except Exception as e:
        print(f"Error umum: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{gen_id}")
async def download_gif(gen_id: str):
    gif_path = Path(f"outputs/{gen_id}/output.gif")
    if not gif_path.exists():
        raise HTTPException(status_code=404, detail="GIF not found")
    
    return FileResponse(
        gif_path,
        media_type="image/gif",
        headers={"Content-Disposition": f'attachment; filename="{gen_id}.gif"'}
    )
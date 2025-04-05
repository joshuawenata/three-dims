import argparse
import torch
from diffusers import ShapEPipeline
from PIL import Image
import os

def generate_gif(prompt: str, output_dir: str) -> str:
    device = "cpu"

    pipe = ShapEPipeline.from_pretrained(
        "openai/shap-e",
        torch_dtype=torch.float32,
    ).to(device)

    num_inference_steps = 63 

    output = pipe(
        prompt,
        guidance_scale=15.0,
        num_inference_steps=num_inference_steps,
    )

    os.makedirs(output_dir, exist_ok=True)

    frames = output.images[0]
    gif_path = os.path.join(output_dir, "output.gif")

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
    )

    return gif_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()

    gif_path = generate_gif(args.prompt, args.output_dir)
    print(f"GIF generated at: {gif_path}")
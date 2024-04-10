# Modal Initalization
from modal import Image, Stub, gpu

stub = Stub(name="outlines-app")

outlines_image = Image.debian_slim(python_version="3.11").pip_install(
    "outlines==0.0.34",
    "transformers==4.38.2",
    "datasets==2.18.0",
    "accelerate==0.27.2",
)

def import_model():
    import outlines

    outlines.models.transformers("mistralai/Mistral-7B-v0.1")


outlines_image = outlines_image.run_function(import_model)

@stub.function(image=outlines_image, gpu=gpu.A100(memory=80), timeout=300)
def generate(schema: str, prompt: str):
    import outlines

    model = outlines.models.transformers(
                    "mistralai/Mistral-7B-v0.1", device="cuda"
                )

    generator = outlines.generate.json(model, schema.strip(), whitespace_pattern="")

    result = generator(prompt)

    return result
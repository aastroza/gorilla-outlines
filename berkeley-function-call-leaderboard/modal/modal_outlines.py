# Modal Initalization
from modal import Image, Stub, build, gpu, enter, method

stub = Stub(name="outlines-app")

outlines_image = Image.debian_slim(python_version="3.11").pip_install(
    "outlines==0.0.34",
    "transformers==4.38.2",
    "datasets==2.18.0",
    "accelerate==0.27.2",
)

@stub.cls(image=outlines_image, gpu=gpu.A100(memory=80), timeout=300)
class Model:
    @build()
    @enter()
    def import_model(self):
        import outlines

        self.model = outlines.models.transformers(
            "mistralai/Mistral-7B-Instruct-v0.2", device="cuda"
        )

    @method()
    def generate(self, schema: str, prompt: str):
        import outlines

        generator = outlines.generate.json(self.model, schema.strip())

        result = generator(prompt)

        return result
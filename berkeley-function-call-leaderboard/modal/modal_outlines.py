from modal import Image, Stub, Secret, build, gpu, enter, method

stub = Stub(name="outlines-app")

outlines_image = Image.debian_slim(python_version="3.11").pip_install(
    "outlines==0.0.37",
    "transformers==4.38.2",
    "datasets==2.18.0",
    "accelerate==0.27.2",
)

@stub.cls(image=outlines_image, secrets=[Secret.from_name("my-huggingface-secret")], gpu=gpu.A100(memory=80), timeout=300)
class Model:
    # @build()
    # @enter()
    # def import_model(self):
    def __init__(self, model_name: str) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from outlines import models
        import os

        llm = AutoModelForCausalLM.from_pretrained(model_name, output_attentions=True, token=os.environ["HF_TOKEN"])
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.environ["HF_TOKEN"])
        self.model = models.Transformers(llm, tokenizer)
        # import outlines
        # self.model = outlines.models.transformers(
        #     model_name, device="cuda"
        # )

    @method()
    def generate(self, schema: str, prompt: str, whitespace_pattern: str = None):
        import outlines

        if whitespace_pattern:
            generator = outlines.generate.json(self.model, schema.strip(), whitespace_pattern=whitespace_pattern)
        else:
            generator = outlines.generate.json(self.model, schema.strip())

        result = generator(prompt)

        return result
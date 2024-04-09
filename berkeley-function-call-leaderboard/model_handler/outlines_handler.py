from auto_gptq import exllama_set_max_input_length
import os, time, json
import outlines

from model_handler.constant import GORILLA_TO_OPENAPI
from model_handler.model_style import ModelStyle
from model_handler.utils import _cast_to_openai_type

class OutlinesHandler:
    model_name: str
    model_style: ModelStyle

    def __init__(self, model_name, temperature=0.7, top_p=1, max_tokens=1000) -> None:
        self.model_name = model_name
        self.model_style = ModelStyle.Outlines
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.model = outlines.models.transformers(model_name, device='cuda')
        self.model.model = exllama_set_max_input_length(self.model.model, max_input_length=4000)
    
    def format_result(self, function_name, result):
        # This method is used to format the result in a standard way.
        args_string = ', '.join([f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}" for key, value in result.items()])
        # Creating the output string with the function name and arguments
        output_string = f'[{function_name}({args_string})]'
        return output_string

    def inference(self, prompt, functions, test_category):
        # IMPORTANT: Only works for 'simple' test_category.
        if type(functions) is not list:
                functions = [functions]
        
        schema = json.dumps({
            "title": functions[0]["name"],
            "type": "object",
            "description": functions[0]["description"],
            "properties": _cast_to_openai_type(functions[0]["parameters"]["properties"], GORILLA_TO_OPENAPI, test_category),
            "required": functions[0]["parameters"]["required"]
        })

        generator = outlines.generate.json(self.model, schema.strip(), whitespace_pattern="")
        # This method is used to retrive model response for each model.
        start_time = time.time()
        try:
            result = generator(
                f""""
            You are an expert in composing functions. You are given a question and a set of possible functions. 
            Based on the question, you will need to make one or more function/tool calls to achieve the purpose. 
            If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
            also point it out. You should only return the function call in tools call sections.
            Question: {prompt}
            """
            )
            result = self.format_result(functions[0]["name"], result)
        except:
            result = '[error.message(error="Error occurred")]'
        latency = time.time() - start_time

        metadata = {}
        metadata["input_tokens"] = None
        metadata["output_tokens"] = None
        metadata["latency"] = latency
        return result, metadata


    def decode_ast(self, result, language="Python"):
        decoded_output = []
        for invoked_function in result:
            name = list(invoked_function.keys())[0]
            params = json.loads(invoked_function[name])
            if language == "Python":
                pass
            else:
                # all values of the json are casted to string for java and javascript
                for key in params:
                    params[key] = str(params[key])
            decoded_output.append({name: params})
        return decoded_output

    def decode_execute(self, result):
        # This method takes raw model output and convert it to standard execute checker input.
        pass

    def write(self, result, file_to_open):
        # This method is used to write the result to the file.
        if not os.path.exists("./result"):
            os.mkdir("./result")
        if not os.path.exists("./result/" + self.model_name.replace("/", "-")):
            os.mkdir("./result/" + self.model_name.replace("/", "-"))
        with open(
            "./result/"
            + self.model_name.replace("/", "-")
            + "/"
            + file_to_open.replace(".json", "_result.json"),
            "a+",
        ) as f:
            f.write(json.dumps(result) + "\n")

    def load_result(self, test_category):
        # This method is used to load the result from the file.
        result_list = []
        with open(
            f"./result/{self.model_name.replace('/', '-')}/gorilla_openfunctions_v1_test_{test_category}_result.json"
        ) as f:
            for line in f:
                result_list.append(json.loads(line))
        return result_list

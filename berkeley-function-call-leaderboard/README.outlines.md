# Berkeley Function Calling Leaderboard

💡 Read more in our [Gorilla OpenFunctions Leaderboard Blog](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)

🦍 Berkeley Function Calling Leaderboard live [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html#leaderboard)

🦍 Berkeley Function Calling Leaderboard on Hugginface [Berkeley Function Calling Leaderboard Huggingface](https://huggingface.co/spaces/gorilla-llm/berkeley-function-calling-leaderboard)

## Introduction
We present Berkeley Function Leaderboard, the **first comprehensive and executable function calling evaluation for LLMs function calling**. Different from prior function calling evaluations (e.g. Anyscale function calling blog), we consider function callings of various forms, different function calling scenarios, and the executability of function calls. We also release our model Gorilla-Openfunctions-v2, the best open-source models so far to handle multiple languages of function calls, parallel function calls and multiple function calls. We also provide a specific debugging feature that when the provided function is not suitable for your task, the model will output an “Error Message”. 

Read more about the technical details and interesting insights in our blog post!

![image](./architecture_diagram.png)
### Install Dependencies

Before generating the leaderboard statistics, you should install dependencies using the following command: 

```bash
    pip install -r requirements.txt # Inside ./berkeley-function-call-leaderboard
```


## Prepare Evaluation Dataset

To download the evaluation dataset from huggingface, from the current directory `./openfunctions/berkeley-function-call-leaderboard`, run the following command:

```bash
    huggingface-cli download gorilla-llm/Berkeley-Function-Calling-Leaderboard --local-dir ./data --repo-type dataset
```


This will download our dataset to `data` repository. 

## Evaluation Dataset

The evaluation datasets are now stored in the `./data` folder. The possible answers are stored in the `./data/possible_answer` folder. 


## Execution Evaluation Data Post-processing 

Then, use `eval_data_compilation.py` to compile all files by using

```bash
    python eval_data_compilation.py
```
## Berkeley Function-Calling Leaderboard Statistics

To generate leaderboard statistics, there are two steps:

1. Inference the evaluation data and obtain the results from specific models 

```bash
    python openfunctions_evaluation.py --model MODEL_NAME --test_category TEST_CATEGORY
```
For TEST_CATEGORY, we have `executable_simple`, `executable_parallel_function`, `executable_multiple_function`, `executable_parallel_multiple_function`, `simple`, `relevance`, `parallel_function`, `multiple_function`, `parallel_multiple_function`, `java`, `javascript`, `rest`, `sql`, `chatable`.

If you want to run all evaluation at the same time, you can use `all` as the test category.

Running proprietary model like GPTs, Claude, Mistral-X will requires an API-Key which can be supplied in `openfunctions_evaluation.py`.

If decided to run OSS model, openfunctions evaluation uses vllm and therefore requires GPU for hosting and inferencing. If you have questions or concerns about evaluating OSS models, please reach out to us in our [discord channel](https://discord.gg/grXXvj9Whz).

## Checking the Evaluation Results

### Running the Checker

Navigate to the `./berkeley-function-call-leaderboard/eval_checker` directory and run the `eval_runner.py` script with the desired parameters. The basic syntax is as follows:

```bash
    python ./eval_runner.py --model MODEL_NAME --test_category {TEST_CATEGORY,all,ast,executable,python,non-python}
```

- `MODEL_NAME`: Optional. The name of the model you wish to evaluate. This parameter can accept multiple model names separated by spaces. Eg, `--model gorilla-openfunctions-v2 gpt-4-0125-preview`.
    - If no model name is provided, the script will run the checker on all models exist in the `./result` folder. This path can be changed by modifying the `INPUT_PATH` variable in the `eval_runner.py` script.
- `TEST_CATEGORY`: Optional. The category of tests to run. You can specify multiple categories separated by spaces. Available options include:
    - `all`: Run all test categories.
    - `ast`: Abstract Syntax Tree tests.
    - `executable`: Executable code evaluation tests.
    - `python`: Tests specific to Python code.
    - `non-python`: Tests for code in languages other than Python, such as Java and JavaScript.
    - Individual test categories:
        - `simple`: Simple function calls.
        - `parallel_function`: Multiple function calls in parallel.
        - `multiple_function`: Multiple function calls in sequence.
        - `parallel_multiple_function`: Multiple function calls in parallel and in sequence.
        - `executable_simple`: Executable function calls.
        - `executable_parallel_function`: Executable multiple function calls in parallel.
        - `executable_multiple_function`: Executable multiple function calls in sequence.
        - `executable_parallel_multiple_function`: Executable multiple function calls in parallel and in sequence.
        - `java`: Java function calls.
        - `javascript`: JavaScript function calls.
        - `rest`: REST API function calls.
        - `relevance`: Function calls with irrelevant function documentation.
    - If no test category is provided, the script will run all available test categories.
> If you want to run the `all` or `executable` or `python` category, make sure to register your REST API keys in `function_credential_config.json`. This is because Gorilla Openfunctions Leaderboard wants to test model's generated output on real world API! 
> If you do not wish to provide API keys for REST API testing, set `test_category` to `ast` or any non-executable category.

### Example Usage

If you want to run all tests for the `gorilla-openfunctions-v2` model, you can use the following command:

```bash
    python ./eval_runner.py --model gorilla-openfunctions-v2
```

If you want to runn `rest` tests for all GPT models, you can use the following command:

```bash
    python ./eval_runner.py --model gpt-3.5-turbo-0125 gpt-4-0613 gpt-4-1106-preview gpt-4-0125-preview --test_category rest
```

If you want to run `rest` and `javascript` tests for all GPT models and `gorilla-openfunctions-v2`, you can use the following command:

```bash
    python ./eval_runner.py --model gorilla-openfunctions-v2 gpt-3.5-turbo-0125 gpt-4-0613 gpt-4-1106-preview gpt-4-0125-preview --test_category rest javascript
```
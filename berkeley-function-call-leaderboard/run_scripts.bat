@echo off
python openfunctions_evaluation.py --model google/gemma-7b-it --test_category simple 
python openfunctions_evaluation.py --model mistralai/Mistral-7B-Instruct-v0.2 --test_category simple
python openfunctions_evaluation.py --model deepseek-ai/deepseek-coder-7b-instruct-v1.5 --test_category simple 
python openfunctions_evaluation.py --model deepseek-ai/deepseek-coder-7b-base-v1.5 --test_category simple 
python openfunctions_evaluation.py --model gorilla-llm/gorilla-openfunctions-v2 --test_category simple 
python openfunctions_evaluation.py --model gorilla-openfunctions-v2 --test_category simple 
python openfunctions_evaluation.py --model gpt-4-0125-preview --test_category simple 
python openfunctions_evaluation.py --model meta-llama/Meta-Llama-3-8B-Instruct --test_category simple 
pause
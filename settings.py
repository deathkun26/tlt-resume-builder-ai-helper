import os
from dotenv import load_dotenv

load_dotenv('.env')

service_interface = os.getenv("SERVICE_INTERFACE")
service_port = os.getenv("SERVICE_PORT")
summary_model_path = os.getenv("SUMMARY_MODEL_PATH")
resume_parser_model_path = os.getenv("RESUME_PARSER_MODEL_PATH")
hf_auth_token = os.getenv("HF_AUTH_TOKEN")
client = os.getenv("CLIENT")
enable_gramformer = os.getenv("ENABLE_GRAMFORMER") == "1"
enable_gpt2 = os.getenv("ENABLE_GPT2") == "1"
enable_bart = os.getenv("ENABLE_BART") == "1"

print("Environment : ------------------------------------- ")
print("service_interface", service_interface)
print("service_port", service_port)
print("summary_model_path", summary_model_path)
print("resume_parser_model_path", resume_parser_model_path)
print("hf_auth_token", hf_auth_token)
print("client", client)
print("enable_gramformer", enable_gramformer)
print("enable_gpt2", enable_gpt2)
print("enable_bart", enable_bart)
print("--------------------------------------------------- ")



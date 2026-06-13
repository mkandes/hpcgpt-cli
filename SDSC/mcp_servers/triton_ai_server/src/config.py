import argparse
from pydantic import BaseModel, Field

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant that can answer questions about high-performance computing (HPC) systems, software, and general HPC concepts. You provide clear, accurate, and concise responses to a wide range of HPC-related topics."
)

class Config(BaseModel):
    host: str = Field(
        default="127.0.0.1", 
        description="The host ip address for the server to listen on")
    port: int = Field(
        default=8001, 
        description="The port for the server to listen on")
    log_file: str = Field(
        default="logs/Latest.log", 
        description="The file to write server logs to")
    triton_ai_url: str = Field(
        description="The URL of the Triton AI API, can also be set with the TRITON_AI_URL environment variable",
        json_schema_extra={"env": "TRITON_AI_URL"})
    triton_ai_api_key: str = Field(
        description="API key for the Triton AI API, can also be set with the TRITON_AI_API_KEY environment variable",
        json_schema_extra={"env": "TRITON_AI_API_KEY"})
    triton_ai_model: str = Field(
        description="The model to use for the Triton AI API, can also be set with the TRITON_AI_MODEL environment variable",
        json_schema_extra={"env": "TRITON_AI_MODEL"})
    triton_ai_system_prompt: str = Field(
        default=DEFAULT_SYSTEM_PROMPT,
        description="System message prepended to each Triton AI API request",
    )

    @classmethod
    def load_from_json(cls, filepath: str = "config.json") -> "Config":
        with open(filepath, "r") as f:
            return cls.model_validate_json(f.read())

def consolidate_config_and_args(config: Config, args: argparse.Namespace):
    # Merge config and args into a single args, with args taking precedence
    for key, value in config.__dict__.items():
        if key.replace("_", "-") not in args.__dict__ or args.__dict__[key] is None:
            args.__dict__[key] = value
    return args

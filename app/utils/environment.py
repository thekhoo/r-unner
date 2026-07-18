from pydantic_settings import BaseSettings, SettingsConfigDict

class RunnerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RUNNER_", extra="ignore")
    
    inputs_s3_uri: str
    outputs_s3_uri: str
    entrypoint: str
    
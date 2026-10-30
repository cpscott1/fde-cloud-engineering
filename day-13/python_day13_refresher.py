import os

def get_environment():
    environment = os.getenv("B2D_ENV", "development")
    return environment

print("Environment:", get_environment())
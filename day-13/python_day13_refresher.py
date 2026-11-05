import os

def get_environment():
    environment = os.getenv("B2D_ENV", "development")
    return environment

print("Environment:", get_environment())

def get_host_port():
    port = os.getenv("B2D_HOST_PORT", "8004")
    port = int(port)
    return port

print("Host port:", get_host_port())

def load_config():
    environment = get_environment()
    host_port = get_host_port()

    config = {
        "environment": environment,
        "host_port": host_port
    }

    return config

config = load_config()
print("Configuration:", config)

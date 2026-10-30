host_port = 8000
container_port = 80

port_mapping = f"{host_port}:{container_port}"
print(port_mapping)

container_config = {
    "name": "b2d-port-test",
    "image": "nginx:alpine",
    "host_port": 8000,
    "container_port": 80,
    "running": True
}

container_config["environment"] = "development"

print(container_config["image"])
print(container_config["running"])
print(container_config["environment"])

print(container_config)

def describe_container(config):
    return f"{config['name']} uses {config['image']} on {config['host_port']}:{config['container_port']}"

description = describe_container(container_config)
print(description)

checks = [
    {"name": "docker_cli", "passed": True},
    {"name": "docker_engine", "passed": True},
    {"name": "http_response", "passed": True},
]

passed = 0
failed_checks = []

for check in checks:
    print(check["name"], check["passed"])
    
    if check["passed"]:
        passed += 1
    else:
        failed_checks.append(check["name"])

print("Passed:", passed)
print("Failed checks:", failed_checks)

if passed == len(checks):
    print("Ready to build B2D image")
else:
    print("Not ready")

def all_checks_passed(checks):
    for check in checks:
        if check["passed"] == False:
            return False

    return True

print(all_checks_passed(checks))

test_checks = [
    {"name": "docker_cli", "passed": True},
    {"name": "docker_engine", "passed": False}
]

print(all_checks_passed(test_checks))


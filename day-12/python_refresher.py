def explain_health(status):

    if status == "starting":
        return "Docker is checking the application"

    elif status == "healthy":
        return "The application's health check is succeeding"

    elif status == "unhealthy":
        return "The application's health check has repeatedly failed"

    else:
        return "The application is giving an unknown health status"

print(explain_health("starting"))
print(explain_health("healthy"))
print(explain_health("unhealthy"))
print(explain_health("unknown"))  

probe_results = [False, True, False]

consecutive_failures = 0

for result in probe_results:
    if result == False:
        consecutive_failures += 1
    else:
        consecutive_failures = 0

print("Consecutive failures:", consecutive_failures)

def count_consecutive_failures(results):
    consecutive_failures = 0

    for result in results:
        if result == False:
            consecutive_failures += 1
        else:
            consecutive_failures = 0

    return consecutive_failures

print("Three failures:", count_consecutive_failures([False, False, False]))
print("Interrupted failures:", count_consecutive_failures([False, True, False]))
print("No failures:", count_consecutive_failures([True, True, True]))

assert count_consecutive_failures([False, False, False]) == 3, "Expected three consecutive failures"

assert count_consecutive_failures([False, True, False]) == 1, "Expected one consecutive failure"

assert count_consecutive_failures([True, True, True]) == 0, "Expected no failures"

print("All three failure-count assertions passed")

assert explain_health("healthy") == "The application's health check is succeeding", "Healthy status is incorrect"

assert explain_health("starting") == "Docker is checking the application", "The application is not starting"

assert explain_health("unhealthy") == "The application's health check has repeatedly failed", "The unhealthy status is incorrect"

assert explain_health("unknown") == "The application is giving an unknown health status", "The unknown status is incorrect"

print("All four health-status assertions passed")
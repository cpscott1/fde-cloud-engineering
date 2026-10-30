# Day 9 Customer Scenario: Docker Daemon Not Reachable

## Scenario
A district IT administrator installs Docker Desktop on a school computer. `docker --version`
works, but `docker run --rm hello-world` reports that it cannot connect to the Docker daemon.

I hit this same issue on Day 9 on my Mac mini (Apple Silicon), so my answers draw on my
own terminal results.

## 1. What is the difference between the Docker CLI being installed and the Docker engine being available?

The Docker CLI is the `docker` command. It's a client program that takes what I type and
sends it as a request to the Docker engine (the daemon). The engine is the background
service that actually pulls images, builds them, and runs containers.

`docker --version` only asks the CLI to report its own version. It never talks to the
engine, so it can pass even when the engine is stopped, still starting, or blocked.
Anything that does real work, like `docker run`, `docker ps`, or `docker info`, needs the
engine, and that's where "cannot connect to the Docker daemon" shows up.

Simple way to explain it to the customer: the CLI is the remote control, the engine is
the TV. The remote can have fresh batteries and still do nothing if the TV is off.

My evidence: on Day 9, `docker --version` returned version 29.8.2, but my first
`docker info` could not connect to the daemon. The CLI was fine; the engine wasn't up yet.

## 2. What would you check first to investigate the problem?

Start with the most likely cause and work outward:

1. **Is Docker Desktop actually running?** Check that the app is open and its status says
   the engine is running, not "starting." This was my exact issue: the engine needed time
   to come up after launch. If it's stuck, quit and restart Docker Desktop.
2. **Run `docker info` and read the Server section.** If only the Client section prints and
   the Server section shows an error, the CLI can't reach the engine. This confirms where
   the problem is before changing anything.
3. **Check the CLI is pointed at the right engine.** Run `docker context ls` and make sure
   the active context is the Docker Desktop one (`desktop-linux` on Mac, `default` or
   `desktop-linux` on Windows).
4. **On a Windows school computer, check the common blockers:**
   - WSL 2 is installed and up to date (`wsl --status`)
   - Virtualization is enabled in the BIOS/UEFI
   - The signed-in user is in the `docker-users` group (a frequent issue when an admin
     installs Docker but a different, standard user account runs it)
   - District security software or group policy isn't blocking Docker's background service
5. **Check Docker Desktop's logs or Troubleshoot menu** if none of the above explains it.

I'd record what I found at each step so the district has a repeatable checklist, not just
a fixed machine.

## 3. What commands or output would prove to the customer that the problem was resolved?

Run these in order and share the real output, matching what I verified on Day 9:

| Check | Command | What proves it passed |
|---|---|---|
| CLI installed | `docker --version` | A version number prints (mine: 29.8.2) |
| Engine reachable | `docker info` | A Server section prints with no connection error |
| Container runs | `docker run --rm hello-world` | The "Hello from Docker!" message prints |
| Networking works | `docker run --rm -d -p 8001:80 nginx` then `curl -I http://localhost:8001` | `HTTP/1.1 200 OK` (mine returned 200 OK on port 8001) |
| Cleanup works | `docker stop <container-id>` then `docker ps` | The nginx container is gone from the list |

The key point for the customer: `docker --version` passing is not proof. The problem is
only resolved when `docker info` shows the server and a real container runs. On Day 9,
my first `docker info` failed, and the later hello-world, ARM64, and nginx tests all
passed. That before-and-after record is the evidence I'd hand back to the district.

## FDE takeaway
Don't call an environment ready because the tool is installed. Prove the engine is
running, a container starts, and a port is reachable, and give the customer the commands
so they can verify it themselves next time.
# Day 13 - Docker Compose Deployment Evidence

## 1. Objective

I deployed the B2D Knowledge Assistant using Docker Compose and practiced
changing the host port for a simulated district port conflict.

## 2. Configuration Validation

I checked the Compose configuration with:

```sh
docker compose config
```

Compose printed the resolved configuration for the `assistant` service with
no errors. It included the build context, image name, port mapping, and
`B2D_KNOWLEDGE_DIR` environment variable. After my port change, the output
showed host address `127.0.0.1`, published port `8010`, and container port
`8000`.

## 3. Initial Deployment

My initial deployment command was:

```sh
docker compose up -d --build
```

- Image: `b2d-knowledge-assistant:day13`
- Service: `assistant`
- Container status: Running (Up)
- Initial host port: `8004` (bound to `127.0.0.1`)
- Container port: `8000`

## 4. Security Verification

I checked the user running inside the container with:

```sh
docker compose exec assistant id
```

My recorded result was:

- UID: `10001` (`appuser`)
- GID: `10001` (`appgroup`)

## 5. Customer Port Conflict

The practice scenario was that a district already had another service using
host port `8004`. This was a simulated customer problem for the lesson.

I changed the host side of the port mapping in `compose.yaml` from `8004`
to `8010` and kept the container port at `8000`:

```yaml
ports:
  - "127.0.0.1:8010:8000"
```

I checked the updated configuration with `docker compose config`, then
applied the change with:

```sh
docker compose up -d --no-build
```

I didn't need to rebuild the application image. The port mapping is runtime
configuration, so I could apply the change using the existing
`b2d-knowledge-assistant:day13` image. The app still listens on `8000` inside
the container.

## 6. Final Verification

I checked the container status and readiness endpoint with:

```sh
docker compose ps
curl -i http://127.0.0.1:8010/ready
```

- Final host port: `8010` (bound to `127.0.0.1`)
- Container port: `8000`
- Docker health status: `healthy`
- HTTP status: `200 OK`
- Knowledge document count: `3`

The port mapping shown by `docker compose ps` was:

```text
127.0.0.1:8010->8000/tcp
```

The readiness response body was:

```json
{"status":"ready","document_count":3}
```

That response confirmed three knowledge documents were loaded. It didn't
list their filenames.

## 7. Customer Explanation

Here's how I'd explain the change to the customer in this practice scenario:

"Port 8004 was already in use, so I changed one line in the Compose file to
make the assistant available on port 8010. The app still runs on port 8000
inside the container. Docker connects the host's port 8010 to that internal
port, so I didn't need to change the app's code or rebuild the image. I
applied the change and confirmed the container was healthy. The readiness
endpoint returned HTTP 200 and reported three knowledge documents loaded."

For this local exercise, I kept the port bound to `127.0.0.1`, so I accessed
the assistant from the same machine.

## 8. Lessons Learned

I learned to separate the host port from the container port. In
`127.0.0.1:8010:8000`, `127.0.0.1` is the host address, `8010` is the host
port, and `8000` is the container port. I can change the host port to avoid
a conflict without changing the image or Python code.

For this change, I used `docker compose up -d --no-build` to apply the
updated configuration without rebuilding the image. I then checked both
the container's health and the readiness endpoint to make sure it worked.
Keeping the deployment settings in the Compose file gives me a repeatable
setup and makes differences between district configurations easier to see.

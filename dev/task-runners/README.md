# Task Runners (remote host)

Deploys [external-mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners) `n8nio/runners` containers that connect to the n8n task broker on the main stack.

## Prerequisites

- The n8n host is deployed with external task runners enabled (see [dev/README.md](../README.md#task-runners)).
- DNS for `n8n-runners.<BASE_DOMAIN>` resolves to the Traefik ingress (same host as `n8n.<BASE_DOMAIN>`).
- `N8N_RUNNERS_AUTH_TOKEN` matches the value in `n8n.env` on the n8n host.

## Setup

From this directory (`dev/task-runners/`), copy the env templates:

```bash
cp task-runners.env.default task-runners.env
cp default.env .env
```

Edit `task-runners.env`:

- Set `N8N_RUNNERS_AUTH_TOKEN` to the same secret as on the n8n host.
- Set `N8N_RUNNERS_TASK_BROKER_URI` to `http://n8n-runners.<BASE_DOMAIN>` (Traefik URL, not a raw `:5679` address). Use `http://`, not `https://`: the runner launcher always upgrades to a plaintext `ws://` connection, so the broker is routed over the HTTP (`web`) entrypoint. See [n8n host configuration](#broker-route-http-only) below.

Edit `.env`:

- Set `RUNNERS_IMAGE_TAG` to match the n8n version on the n8n host (requires n8n >= 1.111.0). Check with:

  ```bash
  docker exec <n8n-container> n8n --version
  ```

## Deploy

```bash
docker compose up --pull always --detach
```

The runner host needs HTTP egress to the Traefik ingress (port 80).

## Broker route (HTTP-only)

The `n8nio/runners` launcher builds its WebSocket URL by forcing the `ws://`
(plaintext) scheme onto `N8N_RUNNERS_TASK_BROKER_URI`, regardless of whether the
URI is `http://` or `https://`. A TLS/`websecure` Traefik route therefore fails
the WebSocket upgrade with `websocket: bad handshake`.

To make this work, the n8n host routes `n8n-runners.<BASE_DOMAIN>` over the HTTP
(`web`) entrypoint to broker port 5679 (see `base/docker-compose.yaml`), and the
runner connects with:

```
N8N_RUNNERS_TASK_BROKER_URI=http://n8n-runners.<BASE_DOMAIN>
```

If your Traefik globally redirects HTTP to HTTPS, exclude `n8n-runners.<BASE_DOMAIN>`
from that redirect so the plaintext WebSocket upgrade can reach the broker.

## Optional

- `N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT` — seconds of inactivity before the runner shuts down (default `15` in the runners image; set to `0` to disable).

**Note:** `http://n8n-runners.<BASE_DOMAIN>/` in a browser will not show a web UI — it is a WebSocket task broker endpoint for runners only. A `Cannot GET /` response there is expected.

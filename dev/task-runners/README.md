# Task Runners (remote host)

Deploys [external-mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners) `n8nio/runners` containers that connect to the n8n task broker on the main stack.

## Prerequisites

- The n8n host is deployed with external task runners enabled (see [dev/README.md](../README.md#task-runners)).
- DNS for `n8n-runners.<BASE_DOMAIN>` resolves to the n8n host (not Traefik).
- The runner host can reach the n8n host on **5679/tcp** (direct broker port, not via Traefik). The n8n host must allow inbound 5679 in its firewall; see [dev/README.md § Firewall](../README.md#firewall).
- `N8N_RUNNERS_AUTH_TOKEN` matches the value in `n8n.env` on the n8n host.

## Setup

From this directory (`dev/task-runners/`), copy the env templates:

```bash
cp task-runners.env.default task-runners.env
cp default.env .env
```

Edit `task-runners.env`:

- Set `N8N_RUNNERS_AUTH_TOKEN` to the same secret as on the n8n host.
- Set `N8N_RUNNERS_TASK_BROKER_URI` to `http://n8n-runners.<BASE_DOMAIN>:5679` (direct broker access, not Traefik).

Edit `.env`:

- Set `RUNNERS_IMAGE_TAG` to match the n8n version on the n8n host (requires n8n >= 1.111.0). Check with:

  ```bash
  docker exec <n8n-container> n8n --version
  ```

## Deploy

```bash
docker compose up --pull always --detach
```

## Broker access

The task broker listens on port **5679** inside the n8n container and is published on the n8n host as `5679:5679`, bypassing Traefik entirely. On the n8n host, allow inbound 5679/tcp in iptables (or equivalent); see [dev/README.md § Firewall](../README.md#firewall).

The `n8nio/runners` launcher connects with a plaintext `ws://` WebSocket upgrade, so the broker URI must be `http://` (not `https://`):

```
N8N_RUNNERS_TASK_BROKER_URI=http://n8n-runners.<BASE_DOMAIN>:5679
```

Verify from the runner host before deploying:

```bash
curl -s http://n8n-runners.<BASE_DOMAIN>:5679/healthz
# {"status":"ok"}
```

After deploy, logs should show a successful WebSocket connection:

```
Connected: ws://n8n-runners.<BASE_DOMAIN>:5679/runners/_ws?id=...
```

## Python stdlib allowlist

Python stdlib modules allowed in the Code node are configured in [`base/task-runners/n8n-task-runners.json`](../../base/task-runners/n8n-task-runners.json) via `N8N_RUNNERS_STDLIB_ALLOW`.

Current allowlist: `json`, `math`, `datetime`, `random`, `re`, `statistics`, `decimal`, `base64`, `io`.

After editing the config, recreate the runner container:

```bash
docker compose up --pull always --detach --force-recreate
```

When bumping `RUNNERS_IMAGE_TAG`, diff against the upstream `n8n-task-runners.json` in the matching n8n release to pick up any structural changes.

## Optional

- `N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT` — seconds of inactivity before the runner shuts down (default `15` in the runners image; set to `0` to disable).

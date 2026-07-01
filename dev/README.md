# Development Configuration
Sets up a development deploy

## Setup
Copy the default env files:

    for file in *.default; do
        cp "$file" "${file%%.default}"
    done
Copy the `.env` file default:

    cp default.env .env

Modify the `.env` file as necessary. Lines that are not commented-out are required, commented lines are optional.

## Deploy
To pull the latest configured docker images, and re-deploy services as necessary, run the following command:

    docker compose up --pull always --detach

To use a CPU-based version of ollama, run the following command:

    docker compose --profile cpu  up --pull always --detach

To use an nvidia GPU-based version of ollama, run the following command:

    docker compose --profile gpu-nvidia up --pull always --detach

## Task Runners

External task runners execute Code node JavaScript/Python in isolated `n8nio/runners` containers. See the [n8n task runner docs](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners).

**n8n host** (this directory):

1. Add `N8N_RUNNERS_AUTH_TOKEN` to `n8n.env` (copy from `n8n.env.default` if needed).
2. Ensure DNS for `n8n-runners.${BASE_DOMAIN}` resolves to Traefik (same as `n8n.${BASE_DOMAIN}`).
3. Redeploy: `docker compose up --pull always --detach`

**Runner host** (separate machine): see [task-runners/README.md](./task-runners/README.md).

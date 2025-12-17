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

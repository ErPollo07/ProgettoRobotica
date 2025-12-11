# Start Docker Compose services in thingsboard/docker directory
Push-Location "$(Split-Path -Parent $PSCommandPath)/../thingsboard/docker"
try {
    docker compose up -d
} finally {
    Pop-Location
}

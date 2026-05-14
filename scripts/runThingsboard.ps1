<#
.SYNOPSIS
	Avvia i container Docker e mostra i log del servizio ThingsBoard.

.DESCRIPTION
	Esegue `docker compose up -d` per avviare i container in background e poi
	segue i log del servizio `thingsboard-ce` con `docker compose logs -f`.

.EXAMPLE
	.\scrips\runThingsboard.ps1

.NOTES
	Assicurarsi che Docker e Docker Compose siano installati e che il file
	`docker-compose.yaml` contenga il servizio `thingsboard-ce`.
#>
docker compose up -d; docker compose logs -f thingsboard-ce

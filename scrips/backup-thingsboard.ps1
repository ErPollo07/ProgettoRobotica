<#
.SYNOPSIS
	Esegue il backup della directory del database ThingsBoard (`tb-postgres`).

.DESCRIPTION
	Ferma i container Docker definiti in `docker-compose.yaml`, crea un file ZIP
	contenente la cartella `tb-postgres` con un timestamp nel nome e lo salva
	nella cartella corrente.

.EXAMPLE
	.\scrips\backup-thingsboard.ps1

.NOTES
	Assicurarsi di avere i permessi necessari per fermare i container e
	per leggere la directory `tb-postgres`.
#>
$date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$zipName = "thingsboard-backup_$date.zip"

Write-Host "[INFO] Stopping containers..."
docker compose down

Write-Host "[INFO] Creating backup: $zipName"
Compress-Archive -Path .\tb-postgres -DestinationPath $zipName

Write-Host "[OK] Backup saved as $zipName"

$date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$zipName = "thingsboard-backup_$date.zip"

Write-Host "[INFO] Stopping containers..."
docker compose down

Write-Host "[INFO] Creating backup: $zipName"
Compress-Archive -Path .\tb-postgres -DestinationPath $zipName

Write-Host "[OK] Backup saved as $zipName"

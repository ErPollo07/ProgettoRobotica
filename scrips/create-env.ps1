# Create a .env file then copy the content of .env.template.txt to it

$envFilePath = "src/flask_server/.env"

if (-Not (Test-Path -Path $envFilePath)) {
    New-Item -ItemType File -Path $envFilePath -Force | Out-Null
    Get-Content "src/flask_server/.env.template.txt" | Set-Content $envFilePath
    Write-Host ".env file created successfully at $envFilePath"
} else {
    Write-Host ".env file already exists at $envFilePath"
}

<#
.SYNOPSIS
	Avvia l'applicazione Flask eseguendo il modulo principale del server.

.DESCRIPTION
	Utilizza l'interprete Python (alias `py` su Windows) per eseguire il modulo
	`src.flask_server.main.py`. Assicurarsi che l'ambiente Python abbia le
	dipendenze elencate in `requirements.txt` installate.

.EXAMPLE
	.\scrips\runServer.ps1

.NOTES
	Per eseguire in un virtual environment attivarlo prima di lanciare lo script.
#>
py src.flask_server.main

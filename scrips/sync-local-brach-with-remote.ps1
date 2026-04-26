<#
.SYNOPSIS
	Sincronizza il branch locale con il remote `origin`.

.DESCRIPTION
	Esegue `git push -u origin <Branch>` e `git push --set-upstream origin <Branch>`
	per impostare l'upstream e caricare il branch specificato.

.PARAMETER Branch
	Nome del branch locale da pushare (obbligatorio).

.EXAMPLE
	.\sync-local-brach-with-remote.ps1 feature/my-branch

#>
param(
	[Parameter(Mandatory=$true, Position=0)]
	[string]$Branch
)

Write-Host -ForegroundColor Red "Branch: $Branch"
Write-Host -ForegroundColor Red "Eseguo: git push -u origin $Branch"
git push -u origin $Branch

Write-Host -ForegroundColor Red "Eseguo: git push --set-upstream origin $Branch"
git push --set-upstream origin $Branch

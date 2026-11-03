# Fallback Windows: esportazione autentica con Word, istanza separata e invisibile.
$ErrorActionPreference = 'Stop'
$rootDemo = Split-Path -Parent $MyInvocation.MyCommand.Path
$jobs = @(
    @('03-burocrazia/modello.docx', '03-burocrazia/work/modello.pdf'),
    @('03-burocrazia/output/relazione-compilata.docx', '03-burocrazia/work/relazione.pdf'),
    @('04-aggiornamento/input/modello/modello_001.docx', '04-aggiornamento/work/prima.pdf'),
    @('04-aggiornamento/output/documenti/modello/modello_001.docx', '04-aggiornamento/work/dopo.pdf')
)
$wordDemo = New-Object -ComObject Word.Application
$wordDemo.Visible = $false
$wordDemo.DisplayAlerts = 0
try {
    foreach ($job in $jobs) {
        $sourceDemo = [IO.Path]::GetFullPath((Join-Path $rootDemo $job[0]))
        $targetDemo = [IO.Path]::GetFullPath((Join-Path $rootDemo $job[1]))
        New-Item -ItemType Directory -Force (Split-Path -Parent $targetDemo) | Out-Null
        $docDemo = $wordDemo.Documents.Open($sourceDemo, $false, $true)
        try { $docDemo.ExportAsFixedFormat($targetDemo, 17) }
        finally { $docDemo.Close(0) }
        Write-Output $targetDemo
    }
}
finally { $wordDemo.Quit() }

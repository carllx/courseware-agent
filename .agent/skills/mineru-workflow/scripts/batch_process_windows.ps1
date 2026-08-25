param(
    [Parameter(Mandatory=$true)]
    [string]$folderPath
)

# anaconda powershell prompt
# Ensure conda is activated, otherwise the script relies on the active environment.
Write-Host "Please ensure Conda environment 'MinerU' is activated before running this script."

Get-ChildItem -Path $folderPath -Filter *.pdf | ForEach-Object {
    $pdfFile = $_.FullName
    $command = "magic-pdf pdf-command --pdf `"$pdfFile`" --inside_model true"
    Write-Host "正在处理文件: $pdfFile"
    Invoke-Expression $command
}

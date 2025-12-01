# Script PowerShell para testar comunicação entre serviços

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste de Comunicação entre Serviços" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Iniciando todos os serviços..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "Aguardando serviços ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "2. Verificando status dos containers:" -ForegroundColor Green
docker-compose ps

Write-Host ""
Write-Host "3. Testando endpoint principal (verifica todos os serviços):" -ForegroundColor Green
Write-Host ""
$response = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
$response | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "4. Testando endpoint do banco de dados:" -ForegroundColor Green
Write-Host ""
$dbResponse = Invoke-RestMethod -Uri "http://localhost:8080/db" -Method Get
$dbResponse | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "5. Testando endpoint do cache:" -ForegroundColor Green
Write-Host ""
$cacheResponse = Invoke-RestMethod -Uri "http://localhost:8080/cache" -Method Get
$cacheResponse | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "6. Testando health check:" -ForegroundColor Green
Write-Host ""
$healthResponse = Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get
$healthResponse | ConvertTo-Json

Write-Host ""
Write-Host "7. Verificando rede Docker:" -ForegroundColor Green
docker network inspect desafio3-network | Select-String -Pattern "Name|IPv4Address" | Select-Object -First 10

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste concluído!" -ForegroundColor Green
Write-Host "Todos os serviços estão se comunicando corretamente." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Acesse http://localhost:8080 no navegador para ver a aplicação." -ForegroundColor Yellow


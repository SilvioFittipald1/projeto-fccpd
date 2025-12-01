# Script PowerShell para testar comunicação entre microsserviços

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste de Microsserviços Independentes" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Iniciando microsserviços..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "Aguardando serviços ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "2. Verificando status dos containers:" -ForegroundColor Green
docker-compose ps

Write-Host ""
Write-Host "3. Testando Microsserviço A (API de Usuários):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:5000/usuarios" -ForegroundColor Gray
Write-Host ""
$responseA = Invoke-RestMethod -Uri "http://localhost:5000/usuarios" -Method Get
Write-Host "Resposta do Microsserviço A:" -ForegroundColor Yellow
$responseA | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "4. Testando Microsserviço B (Agregador):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:5001/usuarios-completos" -ForegroundColor Gray
Write-Host ""
$responseB = Invoke-RestMethod -Uri "http://localhost:5001/usuarios-completos" -Method Get
Write-Host "Resposta do Microsserviço B (consome o A):" -ForegroundColor Yellow
$responseB | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "5. Testando endpoint específico do Microsserviço B:" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:5001/usuario/1" -ForegroundColor Gray
Write-Host ""
$responseB2 = Invoke-RestMethod -Uri "http://localhost:5001/usuario/1" -Method Get
Write-Host "Usuário 1 com informações combinadas:" -ForegroundColor Yellow
$responseB2 | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "6. Verificando health checks:" -ForegroundColor Green
Write-Host ""
Write-Host "Microsserviço A:" -ForegroundColor Yellow
$healthA = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method Get
$healthA | ConvertTo-Json

Write-Host ""
Write-Host "Microsserviço B:" -ForegroundColor Yellow
$healthB = Invoke-RestMethod -Uri "http://localhost:5001/health" -Method Get
$healthB | ConvertTo-Json

Write-Host ""
Write-Host "7. Verificando rede Docker:" -ForegroundColor Green
docker network inspect microsservicos-network | Select-String -Pattern "Name|IPv4Address" | Select-Object -First 10

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste concluído!" -ForegroundColor Green
Write-Host "Microsserviços estão se comunicando corretamente." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Endpoints disponíveis:" -ForegroundColor Yellow
Write-Host "  Microsserviço A: http://localhost:5000" -ForegroundColor Gray
Write-Host "  Microsserviço B: http://localhost:5001" -ForegroundColor Gray


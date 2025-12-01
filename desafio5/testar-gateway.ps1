# Script PowerShell para testar API Gateway e microsserviços

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste de API Gateway e Microsserviços" -ForegroundColor Cyan
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
Write-Host "3. Testando API Gateway (ponto único de entrada):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/" -ForegroundColor Gray
Write-Host ""
$gatewayInfo = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
Write-Host "Informações do Gateway:" -ForegroundColor Yellow
$gatewayInfo | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "4. Testando Gateway - Endpoint /users (orquestra Microsserviço de Usuários):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/users" -ForegroundColor Gray
Write-Host ""
$users = Invoke-RestMethod -Uri "http://localhost:8080/users" -Method Get
Write-Host "Usuários via Gateway:" -ForegroundColor Yellow
$users | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "5. Testando Gateway - Endpoint /users/1 (usuário específico):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/users/1" -ForegroundColor Gray
Write-Host ""
$user1 = Invoke-RestMethod -Uri "http://localhost:8080/users/1" -Method Get
Write-Host "Usuário 1 via Gateway:" -ForegroundColor Yellow
$user1 | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "6. Testando Gateway - Endpoint /orders (orquestra Microsserviço de Pedidos):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/orders" -ForegroundColor Gray
Write-Host ""
$orders = Invoke-RestMethod -Uri "http://localhost:8080/orders" -Method Get
Write-Host "Pedidos via Gateway:" -ForegroundColor Yellow
$orders | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "7. Testando Gateway - Endpoint /orders/1 (pedido específico):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/orders/1" -ForegroundColor Gray
Write-Host ""
$order1 = Invoke-RestMethod -Uri "http://localhost:8080/orders/1" -Method Get
Write-Host "Pedido 1 via Gateway:" -ForegroundColor Yellow
$order1 | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "8. Testando Gateway - Endpoint /orders/user/1 (pedidos de um usuário):" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/orders/user/1" -ForegroundColor Gray
Write-Host ""
$userOrders = Invoke-RestMethod -Uri "http://localhost:8080/orders/user/1" -Method Get
Write-Host "Pedidos do usuário 1 via Gateway:" -ForegroundColor Yellow
$userOrders | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "9. Testando Gateway - Health Check:" -ForegroundColor Green
Write-Host "   Endpoint: http://localhost:8080/health" -ForegroundColor Gray
Write-Host ""
$health = Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get
Write-Host "Status do Gateway e serviços:" -ForegroundColor Yellow
$health | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "10. Testando Gateway - Status detalhado:" -ForegroundColor Green
Write-Host "    Endpoint: http://localhost:8080/status" -ForegroundColor Gray
Write-Host ""
$status = Invoke-RestMethod -Uri "http://localhost:8080/status" -Method Get
Write-Host "Status detalhado de todos os serviços:" -ForegroundColor Yellow
$status | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "11. Verificando rede Docker:" -ForegroundColor Green
docker network inspect gateway-network | Select-String -Pattern "Name|IPv4Address" | Select-Object -First 15

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste concluído!" -ForegroundColor Green
Write-Host "API Gateway está funcionando como ponto único de entrada." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Endpoints disponíveis via Gateway:" -ForegroundColor Yellow
Write-Host "  http://localhost:8080/users" -ForegroundColor Gray
Write-Host "  http://localhost:8080/users/<id>" -ForegroundColor Gray
Write-Host "  http://localhost:8080/orders" -ForegroundColor Gray
Write-Host "  http://localhost:8080/orders/<id>" -ForegroundColor Gray
Write-Host "  http://localhost:8080/orders/user/<user_id>" -ForegroundColor Gray
Write-Host "  http://localhost:8080/health" -ForegroundColor Gray
Write-Host "  http://localhost:8080/status" -ForegroundColor Gray


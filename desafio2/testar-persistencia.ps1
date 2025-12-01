# Script PowerShell para testar persistência no Windows

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste de Persistência de Dados" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Iniciando containers..." -ForegroundColor Yellow
docker-compose up -d postgres

Write-Host ""
Write-Host "Aguardando banco de dados ficar pronto..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "2. Verificando dados iniciais:" -ForegroundColor Green
docker-compose exec -T postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios ORDER BY id;"

Write-Host ""
Write-Host "3. Adicionando novo registro..." -ForegroundColor Yellow
docker-compose exec -T postgres psql -U usuario -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Teste Persistência', 'teste@email.com');"

Write-Host ""
Write-Host "4. Verificando dados após inserção:" -ForegroundColor Green
docker-compose exec -T postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios ORDER BY id;"

Write-Host ""
Write-Host "5. Parando e removendo o container..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "6. Verificando que o volume ainda existe:" -ForegroundColor Green
docker volume ls | Select-String "desafio2_postgres_data"

Write-Host ""
Write-Host "7. Recriando o container (sem volume novo)..." -ForegroundColor Yellow
docker-compose up -d postgres

Write-Host ""
Write-Host "Aguardando banco de dados ficar pronto..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "8. Verificando que os dados persistiram (incluindo o registro de teste):" -ForegroundColor Green
docker-compose exec -T postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios ORDER BY id;"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Teste concluído!" -ForegroundColor Green
Write-Host "Os dados persistiram mesmo após remover o container." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan


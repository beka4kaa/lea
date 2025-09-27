# 🚨 FIX RAILWAY DEPLOYMENT

## ❌ Проблема:
Railway показывает "Error creating build plan with Railpack" вместо использования Docker.

## ✅ Решение:

### 1. Что добавлено:

#### `railway.json` - ПРИНУДИТЕЛЬНЫЙ Docker:
```json
{
  "$schema": "https://railway.app/railway.schema.json",  
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE", 
    "restartPolicyMaxRetries": 3
  }
}
```

#### `Dockerfile` - Улучшенный с динамическим PORT:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
ENV PORT=8000
EXPOSE $PORT
CMD ["sh", "-c", "python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port $PORT"]
```

### 2. На Railway:

#### Вариант A: Текущий проект
1. Settings → источник кода
2. **Убедиться**: подключена ветка `main`
3. **Redeploy** проект
4. Railway ДОЛЖЕН увидеть `railway.json` и использовать `"builder": "DOCKERFILE"`

#### Вариант B: Новый проект (РЕКОМЕНДУЕТСЯ)
1. **Удалить старый проект** на Railway (у него кэш)
2. **New Project** → Deploy from GitHub  
3. Выбрать `beka4kaa/lea`
4. Выбрать ветку `main`
5. Railway увидит `railway.json` → использует Docker

### 3. Проверка локально:
```bash
cd /Users/bekzhan/Documents/projects/mcp/lea
python3 -c "from mcp_ui_aggregator.api.app import app; print('✅ OK')"
# Должно показать: ✅ OK
```

### 4. Если все еще не работает:

#### На Railway:
- Variables → добавить `PORT=8000`
- Settings → Build Command: оставить пустым
- Settings → Start Command: оставить пустым (Docker сам знает)

## 🔥 Почему ТЕПЕРЬ должно работать:

- ✅ **railway.json** принудительно указывает `"builder": "DOCKERFILE"`
- ✅ **Динамический PORT** в Dockerfile
- ✅ **Health check** на `/health`
- ✅ **Приложение работает** локально

---

**Попробуйте заново - Railway ОБЯЗАН использовать Docker!** 🐳
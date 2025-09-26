# 🚀 НОВЫЙ ДЕПЛОЙ - Ветка railway-docker-deploy

## ✅ Что изменилось:

1. **Новая ветка**: `railway-docker-deploy` (без кэша Railway)
2. **ТОЛЬКО Dockerfile**: никаких других конфигураций
3. **Прямой uvicorn**: без промежуточных скриптов
4. **Чистая структура**: только необходимые файлы

## 📁 Файлы в ветке:

- `Dockerfile` ← единственная конфигурация
- `requirements.txt` ← зависимости
- `main.py` ← есть, но не используется
- `.railway-ignore` ← исключения
- `.dockerignore` ← исключения для Docker

## 🐳 Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "mcp_ui_aggregator.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🎯 НОВЫЙ ДЕПЛОЙ на Railway:

### Вариант 1: Новый проект
1. Зайти на [railway.app](https://railway.app)
2. **New Project** → Deploy from GitHub repo
3. Выбрать репозиторий `beka4kaa/lea`
4. **ВАЖНО**: Выбрать ветку `railway-docker-deploy`
5. Railway увидит ТОЛЬКО Dockerfile → автоматически Docker build

### Вариант 2: Переподключить существующий
1. В настройках проекта Railway
2. Settings → Connect Repo
3. Переподключиться к ветке `railway-docker-deploy`

## 🔥 Почему должно работать:

- ❌ Нет railway.json (Railway не может его игнорировать)
- ❌ Нет Procfile (Railway не будет искать скрипты)  
- ❌ Нет start.sh (его физически нет)
- ✅ ТОЛЬКО Dockerfile (Railway ОБЯЗАН использовать Docker)
- ✅ Прямой uvicorn (без промежуточных скриптов)
- ✅ Новая ветка (без кэша старых конфигураций)

**Railway не сможет НИ НА ЧТО сослаться кроме Dockerfile!** 🐳

---

**Попробуйте деплой с новой ветки `railway-docker-deploy`**
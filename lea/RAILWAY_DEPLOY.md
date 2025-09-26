# Railway Deployment Instructions

## Quick Deploy

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure deployment:**
   - Select this repository
   - Railway will automatically detect the configuration from `railway.json`
   - It will use Docker build with `Dockerfile.railway`

3. **Environment Variables (optional):**
   - No environment variables are required for basic deployment
   - Database will be created automatically as SQLite file

4. **Deploy:**
   - Railway will build and deploy automatically
   - Check logs for any issues
   - Access your app at the provided Railway URL

## Health Check

Once deployed, check:
- `/health` - Health check endpoint
- `/` - Root endpoint with API info
- `/docs` - Swagger documentation

## Files for Railway:

- `railway.json` - Railway configuration
- `Dockerfile.railway` - Docker build configuration  
- `requirements.txt` - Python dependencies
- `server.py` - Application startup script
- `.railwayignore` - Files to exclude from deployment

## Troubleshooting

If deployment fails:
1. Check Railway logs in the dashboard
2. Verify all files are committed to git
3. Ensure requirements.txt has correct dependencies
4. Check that server.py can import all modules

## Local Testing

Test locally before deploying:
```bash
python3 server.py
```

Then visit http://localhost:8000/health
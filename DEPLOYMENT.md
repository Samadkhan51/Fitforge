# FitForge Agent Deployment Guide

## Railway Deployment

### Required Environment Variables

Set these in your Railway project's **Variables** tab:

1. **GOOGLE_API_KEY** - Your Google AI API key
   - Get one from: https://makersuite.google.com/app/apikey
   - Example: `AIzaSyC...` (your actual key)

2. **DATABASE_URL** - PostgreSQL connection string (if using external DB)
   - Format: `postgresql://username:password@host:port/database`
   - If using Railway's PostgreSQL addon, this is automatically set

### Steps to Deploy:

1. **Connect Repository to Railway**
   - Go to Railway.app
   - Create new project
   - Connect your GitHub repository

2. **Set Environment Variables**
   - In your Railway project dashboard
   - Go to "Variables" tab
   - Add: `GOOGLE_API_KEY=your_actual_api_key_here`

3. **Deploy**
   - Railway will automatically detect the Dockerfile
   - The deployment should now work without the .env error

### Local Development

For local development, create a `.env` file in the `FitForge-Agent` directory:

```bash
# .env file for local development
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=postgresql://fitforge:fitforgepassword@localhost:5432/fitforgedb
```

### Troubleshooting

- **"GOOGLE_API_KEY not found"**: Ensure the environment variable is set in Railway's Variables tab
- **Database connection errors**: Check DATABASE_URL environment variable
- **Import errors**: Make sure all dependencies are in requirements.txt

### API Endpoints

Once deployed, your app will have these endpoints:
- `GET /` - Main frontend page
- `POST /chat` - Chat with the fitness agent
- `POST /generate-plan` - Generate a fitness plan
- `GET /static/*` - Static files (CSS, JS)

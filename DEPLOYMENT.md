# 🚀 AI Knowledge Base - Production Deployment Guide

## Railway Deployment (Recommended)

### Step 1: Sign Up for Railway
1. Go to [Railway.app](https://railway.app/)
2. Sign up with your GitHub account
3. Connect your GitHub repository

### Step 2: Deploy Your App
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `ai-knowledge-database` repository
4. Railway will automatically detect the Dockerfile.prod

### Step 3: Add Services
1. **PostgreSQL Database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will provide `DATABASE_URL`

2. **Redis Cache**:
   - Click "New" → "Database" → "Redis"
   - Railway will provide `REDIS_URL`

### Step 4: Configure Environment Variables
In your Railway project settings, add these environment variables:

```bash
# OpenAI API Key
OPENAI_API_KEY=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

# Database (Railway will provide this)
DATABASE_URL=${{RAILWAY_DATABASE_URL}}

# Redis (Railway will provide this)
REDIS_URL=${{RAILWAY_REDIS_URL}}

# Security (generate a random string)
SECRET_KEY=your-super-secret-key-here

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=AI Knowledge Base

# CORS (Railway will provide this)
BACKEND_CORS_ORIGINS=${{RAILWAY_PUBLIC_DOMAIN}}
```

### Step 5: Deploy
1. Railway will automatically build and deploy
2. Your app will be available at: `https://your-app-name.railway.app`
3. API docs at: `https://your-app-name.railway.app/docs`

## Alternative: Render Deployment

### Step 1: Sign Up for Render
1. Go to [Render.com](https://render.com/)
2. Sign up and connect GitHub

### Step 2: Create Services
1. **Web Service**:
   - Connect your repository
   - Build Command: `docker build -f Dockerfile.prod -t ai-knowledge-base .`
   - Start Command: `./start-prod.sh`

2. **PostgreSQL Database**:
   - Create new PostgreSQL database
   - Note the connection string

3. **Redis Instance**:
   - Create new Redis instance
   - Note the connection string

### Step 3: Environment Variables
Set the same environment variables as Railway above.

## Custom Domain (Optional)

### Step 1: Buy Domain
1. Go to [Namecheap](https://www.namecheap.com/) or [Google Domains](https://domains.google/)
2. Purchase your domain (e.g., `yourcompany-knowledge.com`)

### Step 2: Configure DNS
1. In your domain provider, add a CNAME record:
   - Name: `@` (or `www`)
   - Value: `your-app-name.railway.app`

### Step 3: Add Domain to Railway
1. In Railway dashboard, go to Settings
2. Add your custom domain
3. Railway will provide SSL certificate automatically

## Team Access

Once deployed, share the URL with your team:
- **App URL**: `https://your-app-name.railway.app`
- **API Docs**: `https://your-app-name.railway.app/docs`

### Team Onboarding
1. Share the app URL
2. Team members can immediately start:
   - Uploading documents
   - Searching the knowledge base
   - No local setup required!

## Monitoring & Maintenance

### View Logs
- Railway: Go to your project → "Deployments" → View logs
- Render: Go to your service → "Logs" tab

### Database Management
- Railway: Built-in database dashboard
- Render: Use pgAdmin or similar tool

### File Storage
- Files are stored in the container
- For production, consider upgrading to cloud storage (S3, etc.)

## Cost Estimation

### Railway
- **Free Tier**: $5 credit monthly
- **Pro Plan**: $20/month (recommended for teams)
- **Database**: Included
- **Domain**: $1-2/month

### Render
- **Free Tier**: Available (with limitations)
- **Starter Plan**: $7/month
- **Database**: $7/month
- **Domain**: $1-2/month

## Troubleshooting

### Common Issues
1. **Build Fails**: Check logs in Railway/Render dashboard
2. **Database Connection**: Verify DATABASE_URL is set correctly
3. **OpenAI API Errors**: Check API key and billing
4. **File Upload Issues**: Check MAX_FILE_SIZE setting

### Getting Help
1. Check Railway/Render logs
2. Review API documentation at `/docs`
3. Create an issue in the GitHub repository

## Security Considerations

### Production Checklist
- [ ] Change default SECRET_KEY
- [ ] Set up proper CORS origins
- [ ] Enable HTTPS (automatic with Railway/Render)
- [ ] Regular database backups
- [ ] Monitor API usage and costs
- [ ] Set up error monitoring (Sentry, etc.)

---

**Your AI Knowledge Base is now live and accessible to your entire team! 🎉**

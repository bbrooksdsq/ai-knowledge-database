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

### Step 4: Configure Environment Variables (SECURE METHOD)
In your Railway project settings, add these environment variables:

**🔐 IMPORTANT: Never commit API keys to GitHub!**

```bash
# OpenAI API Key (Add your actual key here in Railway dashboard)
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE

# Database (Railway will provide this automatically)
DATABASE_URL=${{RAILWAY_DATABASE_URL}}

# Redis (Railway will provide this automatically)
REDIS_URL=${{RAILWAY_REDIS_URL}}

# Security (generate a random string like: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-here

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=AI Knowledge Base

# CORS (Railway will provide this automatically)
BACKEND_CORS_ORIGINS=${{RAILWAY_PUBLIC_DOMAIN}}
```

### Step 5: Add Your OpenAI API Key Securely
1. In Railway dashboard, go to your project
2. Click on "Variables" tab
3. Add new variable:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `YOUR_ACTUAL_API_KEY_FROM_OPENAI`
4. Click "Add"

**✅ This way your API key is:**
- Never visible in your code
- Never committed to GitHub
- Only accessible to your deployed app
- Secure and encrypted in Railway's system

### Step 6: Deploy
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
Set the same environment variables as Railway above, using Render's dashboard.

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

## Security Best Practices

### ✅ What We're Doing Right
- API keys stored as environment variables (never in code)
- HTTPS enabled automatically
- CORS properly configured
- Database credentials managed by hosting platform

### 🔒 Additional Security Recommendations
- [ ] Change default SECRET_KEY to a random string
- [ ] Set up proper CORS origins
- [ ] Regular database backups
- [ ] Monitor API usage and costs
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Enable 2FA on your OpenAI account
- [ ] Regularly rotate API keys

---

**Your AI Knowledge Base is now live and accessible to your entire team! 🎉**

**🔐 Your API key is secure and never exposed in your code!**

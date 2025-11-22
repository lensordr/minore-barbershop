# Deployment Guide

## 🚀 Deploy to Render

### 1. Push to GitHub
```bash
# Create GitHub repository first, then:
git remote add origin https://github.com/YOUR_USERNAME/minore-barbershop.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` configuration
5. Click "Deploy"

### 3. After Deployment
- Your app will be live at: `https://your-app-name.onrender.com`
- Admin access: `https://your-app-name.onrender.com/admin/login`
- Login: `admin` / `minore123`

## 📝 Manual Setup Required
Since the database is clean, you need to add:
1. **Barbers** - Go to Staff Management
2. **Services** - Add services with pricing
3. **Schedule** - Set business hours

## 🔧 Environment Variables (Optional)
For email functionality, add in Render dashboard:
- `SMTP_SERVER`
- `SMTP_PORT` 
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `FROM_EMAIL`

## 📱 QR Code Access
After deployment, generate QR code pointing to:
`https://your-app-name.onrender.com/book`
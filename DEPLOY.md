# Deploy to Render

## Quick Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the MINORE-BARBERSHOP repository

3. **Configure Service**
   - **Name**: `minore-barbershop`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python setup.py`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free tier is sufficient for testing

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your app will be available at: `https://minore-barbershop.onrender.com`

## Access URLs
- **Customer Booking**: `https://your-app.onrender.com/book`
- **Admin Dashboard**: `https://your-app.onrender.com/admin/login`
- **Default Admin**: `admin` / `minore123`

## Important Notes
- Free tier sleeps after 15 minutes of inactivity
- Database resets on each deployment (SQLite limitation)
- For production, consider upgrading to paid tier with persistent storage
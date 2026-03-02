# 🔍 Sentry Error Monitoring Setup Guide

## What is Sentry?

Sentry is a real-time error tracking system that helps you:
- 🐛 Catch bugs before users report them
- 📊 Track error frequency and impact
- 🔍 Debug with full stack traces
- 📈 Monitor application performance
- 👥 See which users are affected

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Sentry Account

1. Go to [sentry.io](https://sentry.io)
2. Sign up for free account
3. Create new project → Select "FastAPI"
4. Copy your DSN (looks like: `https://xxxxx@xxxxx.ingest.sentry.io/xxxxx`)

### Step 2: Add to Render

1. Go to Render Dashboard
2. Select your service
3. Go to "Environment" tab
4. Add environment variable:
   - Key: `SENTRY_DSN`
   - Value: `<your-sentry-dsn>`
5. Add environment variable:
   - Key: `ENVIRONMENT`
   - Value: `production`
6. Save changes (will trigger redeploy)

### Step 3: Verify

1. After deployment, check Render logs for: `✅ Sentry initialized`
2. Go to Sentry dashboard
3. You should see your app connected

---

## 📊 What Gets Tracked

### Automatically Tracked:
- ✅ All unhandled exceptions
- ✅ Database errors
- ✅ API endpoint errors
- ✅ Performance metrics (10% sample)
- ✅ Request context (URL, method, headers)
- ✅ User context (when available)

### Filtered Out (Privacy):
- ❌ Passwords
- ❌ API keys
- ❌ Authorization headers
- ❌ Cookie values
- ❌ Personal data (PII)

---

## 🎯 How to Use

### View Errors:

1. Go to Sentry dashboard
2. Click "Issues" to see all errors
3. Click any error to see:
   - Full stack trace
   - Request details
   - User context
   - Breadcrumbs (what led to error)
   - Frequency and impact

### Set Up Alerts:

1. Go to "Alerts" in Sentry
2. Create alert rule:
   - "When error occurs more than X times"
   - "When new error type appears"
   - "When error affects X% of users"
3. Choose notification method (email, Slack, etc.)

### Track Performance:

1. Go to "Performance" tab
2. See slowest endpoints
3. Identify bottlenecks
4. Optimize based on data

---

## 🔧 Manual Error Tracking

You can manually track errors in your code:

```python
from sentry_config import capture_exception, capture_message, add_breadcrumb

# Track an exception
try:
    risky_operation()
except Exception as e:
    capture_exception(e, context={
        "user_id": user.id,
        "operation": "booking"
    })

# Track a message (not an error)
capture_message("User completed checkout", level="info", context={
    "revenue": 25.00
})

# Add breadcrumb for debugging
add_breadcrumb(
    message="User selected barber",
    category="user_action",
    data={"barber_id": 5}
)
```

---

## 📈 Monitoring Best Practices

### Daily:
- Check for new error types
- Review high-frequency errors
- Monitor error rate trends

### Weekly:
- Review performance metrics
- Check slow endpoints
- Analyze user impact

### Monthly:
- Review error resolution rate
- Analyze trends
- Update alert rules

---

## 🚨 Common Errors to Watch

### Critical (Fix Immediately):
- Database connection errors
- Payment processing errors
- Authentication failures
- Data corruption

### High Priority:
- Appointment booking failures
- Email sending failures
- Double booking attempts
- VIP code validation errors

### Medium Priority:
- UI rendering errors
- Non-critical API failures
- Performance degradation

### Low Priority:
- Cosmetic issues
- Non-blocking warnings
- Edge case errors

---

## 💰 Pricing

### Free Tier (Recommended for Start):
- 5,000 errors/month
- 10,000 performance transactions/month
- 30-day data retention
- 1 project
- **Perfect for small businesses**

### Paid Tiers:
- Start at $26/month
- More errors/transactions
- Longer retention
- More projects
- Priority support

---

## 🔒 Security & Privacy

### What Sentry Sees:
- Error messages and stack traces
- Request URLs and methods
- Non-sensitive headers
- Performance metrics

### What Sentry DOESN'T See:
- Passwords
- Credit card numbers
- API keys
- Personal data (filtered)
- Cookie values

### Data Location:
- Stored in US (default)
- EU hosting available
- GDPR compliant
- SOC 2 certified

---

## 🎓 Example Alerts to Set Up

### 1. New Error Alert
```
When: New issue is created
Then: Send email to dev team
```

### 2. High Frequency Alert
```
When: Issue occurs more than 10 times in 1 hour
Then: Send Slack notification
```

### 3. User Impact Alert
```
When: Issue affects more than 5% of users
Then: Send urgent email
```

### 4. Performance Alert
```
When: Endpoint response time > 2 seconds
Then: Send notification
```

---

## 📊 Sample Dashboard

After setup, you'll see:

```
Today's Overview:
- 3 new issues
- 45 total errors
- 2 resolved issues
- 98.5% error-free sessions

Top Issues:
1. DatabaseConnectionError (15 occurrences)
2. ValidationError (12 occurrences)
3. TimeoutError (8 occurrences)

Slowest Endpoints:
1. /admin/dashboard (1.2s avg)
2. /api/available-times (0.8s avg)
3. /client/book (0.6s avg)
```

---

## 🔗 Useful Links

- [Sentry Dashboard](https://sentry.io)
- [Sentry Docs](https://docs.sentry.io/)
- [FastAPI Integration](https://docs.sentry.io/platforms/python/guides/fastapi/)
- [Performance Monitoring](https://docs.sentry.io/product/performance/)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Sentry DSN added to Render environment
- [ ] App redeployed successfully
- [ ] Logs show "✅ Sentry initialized"
- [ ] Sentry dashboard shows app connected
- [ ] Test error appears in Sentry (optional)
- [ ] Alerts configured
- [ ] Team members invited

---

## 🆘 Troubleshooting

### "Sentry not initialized"
- Check SENTRY_DSN is set in Render
- Verify DSN format is correct
- Check Render logs for errors

### "No errors appearing"
- Good news! No errors 🎉
- Or: Check Sentry project is correct
- Verify DSN matches project

### "Too many errors"
- Review and fix critical issues first
- Consider increasing error quota
- Set up better error handling

---

## 📞 Support

- Sentry Support: support@sentry.io
- Documentation: docs.sentry.io
- Community: forum.sentry.io

---

**Status:** ✅ Configured (needs SENTRY_DSN)
**Last Updated:** 2024
**Maintainer:** Development Team

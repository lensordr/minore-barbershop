import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import os

def init_sentry():
    """Initialize Sentry error monitoring with FastAPI integration"""
    
    # Use environment variable or fallback to provided DSN
    sentry_dsn = os.environ.get(
        'SENTRY_DSN',
        'https://9e0c59962edd3afdd136b8cb7f5fafad@o4510975167168512.ingest.de.sentry.io/4510975169724496'
    )
    
    if not sentry_dsn:
        print("⚠️  SENTRY_DSN not configured - error monitoring disabled")
        return False
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        
        # Environment
        environment=os.environ.get('ENVIRONMENT', 'production'),
        
        # FastAPI Integration (auto-enabled)
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
        ],
        
        # Performance Monitoring - capture 10% of transactions
        traces_sample_rate=0.1,
        
        # Capture user data (IP, headers) for better debugging
        send_default_pii=True,
        
        # Release tracking
        release=os.environ.get('RENDER_GIT_COMMIT', 'unknown'),
    )
    
    print(f"✅ Sentry initialized - Environment: {os.environ.get('ENVIRONMENT', 'production')}")
    print(f"   DSN: {sentry_dsn[:50]}...")
    return True

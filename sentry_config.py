import sentry_sdk
import os

def init_sentry():
    """Initialize Sentry error monitoring with FastAPI integration"""
    
    sentry_dsn = os.environ.get('SENTRY_DSN', '')
    
    if not sentry_dsn:
        print("⚠️  SENTRY_DSN not configured - error monitoring disabled")
        return False
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        
        # Environment
        environment=os.environ.get('ENVIRONMENT', 'production'),
        
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

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import os

def init_sentry():
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if not sentry_dsn:
        print("⚠️  SENTRY_DSN not configured")
        return False
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=os.environ.get('ENVIRONMENT', 'production'),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False
    )
    print("✅ Sentry initialized")
    return True

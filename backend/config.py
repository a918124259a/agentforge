"""
AgentForge configuration.
"""
import os

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Plans
PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "rate_limit": 10,  # requests/day
        "max_tokens": 1000,
        "stripe_price_id": None
    },
    "starter": {
        "name": "Starter",
        "price": 19,
        "rate_limit": 500,
        "max_tokens": 10000,
        "stripe_price_id": "price_starter"
    },
    "pro": {
        "name": "Pro",
        "price": 49,
        "rate_limit": 2000,
        "max_tokens": 50000,
        "stripe_price_id": "price_pro"
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 199,
        "rate_limit": 10000,
        "max_tokens": 500000,
        "stripe_price_id": "price_enterprise"
    }
}

# Limits
RATE_LIMIT_WINDOW = 86400  # 24 hours in seconds

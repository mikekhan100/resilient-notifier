from fastapi import FastAPI, HTTPException
import random
from circuit_breaker import CircuitBreaker

app = FastAPI()

# Initialize the breaker: Trip after 3 fails, wait 10 seconds to retry
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

def third_party_sms_provider():
    """
    Simulates a service like Twilio.
    We'll make it fail 70% of the time to force the circuit to trip.
    """
    if random.random() < 0.7:
        print("--- ⚠️  Third-party service just crashed! ---")
        raise Exception("Service Unavailable")
    
    return "SMS Sent successfully!"

@app.get("/send-notification")
def send_notification():
    try:
        # We wrap the dangerous call in our breaker
        result = breaker.call(third_party_sms_provider)
        return {"status": "online", "message": result}
    
    except Exception as e:
        # If the breaker is OPEN, this returns a 503 instantly
        # without even trying to hit the provider.
        raise HTTPException(
            status_code=503, 
            detail=f"System Safeguard: {str(e)}"
        )
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_driver_alert(message_body: str):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")
    to_number = os.getenv("DRIVER_PHONE")

    # If Twilio not configured
    if not all([account_sid, auth_token, from_number, to_number]):
        return "ℹ️ WhatsApp not configured. Showing in-app notification only."

    try:
        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        return f"✅ WhatsApp sent successfully (SID: {msg.sid})"

    except Exception as e:
        error_msg = str(e)

        # Detect daily limit
        if "exceeded the" in error_msg.lower():
            return (
                "⚠️ WhatsApp limit reached.\n"
                "Driver notified inside the system instead."
            )

        return f"❌ Notification failed: {error_msg}"

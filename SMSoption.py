from twilio.rest import Client

account_sid = "VOTRE_SID"
auth_token = "VOTRE_TOKEN"
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="🚨 ALERTE INCENDIE détectée ! Vérifiez la carte ForestGuard.",
    from_="+1234567890",
    to="+212XXXXXXXXX"
)

print(message.sid)

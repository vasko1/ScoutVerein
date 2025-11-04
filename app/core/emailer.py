from app.core.settings import settings

def send_email(subject: str, body: str, to: str | None = None):
    # Demo: Ausgabe in der Konsole als "E-Mail"
    recipient = to or settings.EMAIL_ADMIN
    print(f"""
==== EMAIL (DEMO) ====
To: {recipient}
From: {settings.EMAIL_SENDER}
Subject: {subject}

{body}
======================
""")
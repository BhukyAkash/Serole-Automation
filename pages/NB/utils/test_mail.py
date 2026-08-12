import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")  # D:\Automation\pages

def send_email():
    sender_email = "akash.bhukya@serole.com"
    app_password = "Vijay@8790905840"

    #Emails
    to_emails = [""]
    cc_emails = ["akash.bhukya@serole.com"]

    today_date = datetime.now().strftime("%d/%m/%Y")

    msg = EmailMessage()
    msg["Subject"] = "[UAT] - SAP & TIPs - Daily Health Check - " + today_date
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)    

    msg.set_content("")

    msg.add_alternative("""
    <html>
    <body style="font-family: Aptos, sans-serif; font-size: 14px;">
        <p>Hi UAT Team,</p>
        <p>I wanted to inform you that, as part of the UAT system stability, we conducted a Regression Testing and confirmed that the system is stable. You can begin your work without any issues.</p>
        <p>Please find the attached UAT Stability report.</p>
        <br>
        <p style="margin: 0;">Thanks &amp; Regards,</p>
        <p style="margin: 0; color: #E87722;"><strong>Akash Bhukya</strong></p>
        <br>
        <p style="margin: 0;">Serole Associate</p>
        <p style="margin: 0;"><strong>Serole Technologies</strong></p>
        <p style="margin: 0;">+91-8790905840</p>
        <p style="margin: 0;"><a href="mailto:akash.bhukya@serole.com" style="color: #1155CC;">akash.bhukya@serole.com</a></p>

    </body>
    </html>
    """, subtype="html")

    with open(os.path.join(BASE_DIR, "UATStability.xlsx"), "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="UATStability.xlsx"
        )

    with smtplib.SMTP("smtp.office365.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, app_password)
        smtp.send_message(msg, to_addrs=to_emails + cc_emails)

    print("\nEmail sent successfully")
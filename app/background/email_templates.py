from email.message import EmailMessage

def reminder_email_template(title: str, email: str, due_date: str) -> EmailMessage:
    subject = f"Reminder: Task '{title}' is due soon!"
    plain_text = f"Hey! Just a reminder: ypur task '{title}' is due at {due_date}."

    html_content = f"""
    <html>
        <body>
            <h2>Task Reminder 🚀</h2>
            <p>Your task <strong>{title}</strong> is due at <strong>{due_date}</strong>.</p>
        </body>
    </html>
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["To"] = email

    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype="html")

    return msg
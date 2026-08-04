import smtplib
from fastapi import HTTPException,status
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings



def send_verification_email(
    recipient_email: str,
    verification_link: str
):
    message = MIMEMultipart()

    message["From"] = settings.SMTP_EMAIL
    message["To"] = recipient_email
    message["Subject"] = "Verify your Banking API Account"

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🏦 Welcome to Banking API</h2>

            <p>Thank you for registering.</p>

            <p>Please click the button below to verify your email.</p>

            <a
                href="{verification_link}"
                style="
                    background:#2563eb;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;
                    display:inline-block;
                "
            >
                Verify Email
            </a>

            <p style="margin-top:20px;">
                This verification link expires in <b>15 minutes</b>.
            </p>

            <p>If you didn't create this account, you can safely ignore this email.</p>

        </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    server = None

    try:
        server = smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT
        )

        server.starttls()

        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )

        server.sendmail(
            from_addr=settings.SMTP_EMAIL,
            to_addrs=recipient_email,
            msg=message.as_string()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {str(e)}"
        )

    finally:
        if server:
            server.quit()


def send_verification_reset_password(
    recipient_email: str,
    reset_password_link: str
):
    message = MIMEMultipart()

    message["From"] = settings.SMTP_EMAIL
    message["To"] = recipient_email
    message["Subject"] = "Reset the Password"

    html = f"""
<html>
    <body style="font-family: Arial, sans-serif;">
        <h2>🔒 Reset Your Banking API Password</h2>

        <p>We received a request to reset your password.</p>

        <p>Click the button below to create a new password.</p>

        <a
            href="{reset_password_link}"
            style="
                background:#dc2626;
                color:white;
                padding:12px 20px;
                text-decoration:none;
                border-radius:6px;
                display:inline-block;
            "
        >
            Reset Password
        </a>

        <p style="margin-top:20px;">
            This password reset link expires in <b>15 minutes</b>.
        </p>

        <p>
            If you didn't request a password reset, you can safely ignore this email.
            Your password will remain unchanged.
        </p>

        <hr>

        <p style="font-size:12px;color:#666;">
            For security reasons, this link can only be used once.
        </p>

    </body>
</html>
"""
    message.attach(MIMEText(html, "html"))
    server = None
    try:
        server = smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT
        )
        server.starttls()
        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )
        server.sendmail(
            from_addr=settings.SMTP_EMAIL,
            to_addrs=recipient_email,
            msg=message.as_string()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send reset_password_link: {str(e)}"
        )
    finally:
        if server:
            server.quit()
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import os

load_dotenv()


class Mail:
    def __init__(self):
        self.__mail_user_name = str(os.getenv("MAIL_USERNAME"))
        self.__mail_password = str(os.getenv("MAIL_PASSWORD"))
        self.__mail_port= os.getenv("MAIL_PORT")
        self.__mail_server = str(os.getenv("MAIL_SERVER"))

    def setup_connection_config(self):
        return ConnectionConfig(
            MAIL_USERNAME = self.__mail_user_name,
            MAIL_PASSWORD = self.__mail_password,
            MAIL_FROM = self.__mail_user_name,
            MAIL_PORT = self.__mail_port,
            MAIL_SERVER = self.__mail_server,
            MAIL_SSL_TLS = True,
            MAIL_STARTTLS = False,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = True
        )   

    def mail_body(self, email: str, verification_code: str):
        return MessageSchema(
            subject = "New account verification code.",
            recipients = [email],
            body = f"Your verification code is : {verification_code}",
            subtype = "plain"
        )
    async def send_mail(self, email: str, verification_code: str):
        try:
            connection_configuration = self.setup_connection_config()
            mail_content = self.mail_body(email, verification_code)
            mail = FastMail(connection_configuration)
            await mail.send_message(mail_content)
            return {"message": "Verification code sent successfully."}
        except Exception as error:
            raise HTTPException(status_code=500, detail={"error : " : str(error)})

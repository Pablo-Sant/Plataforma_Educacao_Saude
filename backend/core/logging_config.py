import logging
import sys
from logging.handlers import SMTPHandler

def config_logging():
    
    format = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
    
    
    email_handler = SMTPHandler(
        mailhost=("smtp.gmail.com", 587),
        fromaddr="sistema@empresa.com",
        toaddrs=["devs@empresa.com"],
        subject="Erro crítico na aplicação",
        credentials=("usuario", "senha"),
        secure=()
    )
    
    email_handler.setLevel(logging.CRITICAL)
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(filename="logs/app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    stream_handler.setFormatter(format)
    file_handler.setFormatter(format)
    
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(email_handler)
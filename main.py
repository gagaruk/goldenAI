import os
import requests
import hashlib
import smtplib
from email.message import EmailMessage

import logging
import logging.handlers


# =======================
# Logging
# =======================

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# =======================
# Constants
# =======================

URL = "https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf"
HASH_PATH = "manual_hash.txt"

EMAIL_FROM = "teamgoldenhorn@gmail.com"
EMAIL_TO = "teamgoldenhorn@gmail.com"

try:
    EMAIL_PASSWORD = "mzzs zkrx yuem uxbv"

except:
    print("EMAIL_PASSWORD TOKEN NOT FOUND")

# =======================
# Functions
# =======================

def get_hash(content: bytes) -> str:        #turns file to hash
    return hashlib.sha256(content).hexdigest()


def send_mail():            #sends mail
    msg = EmailMessage()
    msg["Subject"] = "FRC Game Manual Güncellendi!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(
        "FRC Game Manual değişti.\n"
        "Golden AI sistemine manuel olarak yeni manuali yüklemen gerekiyor."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)


# =======================
#  Main
# =======================


response = requests.get(URL)
new_content = response.content
new_hash = get_hash(new_content)

old_hash = None
if os.path.exists(HASH_PATH):
    with open(HASH_PATH, "r") as f:
        old_hash = f.read().strip()

if new_hash != old_hash:

    with open(HASH_PATH, "w") as f:
        f.write(new_hash)

    send_mail()
    logger.info('Manual değişti → mail gönderildi.')
else:
    logger.info('Manual değişmedi')


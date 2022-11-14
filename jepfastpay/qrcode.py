import re
import os
import qrcode
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
from PIL import Image

ID_METHOD = "2"
SEPARATOR = ";"

def sanitize_target(target: str = "") -> str:
    """
    Format target, allow only numeric character e.g.

    | - "012345678901234" => "012345678901234"
    | - "080-123-4567" => "0801234567"
    | - "1-1111-11111-11-1" => "1111111111111"
    | - "+66-89-123-4567" => "66891234567"

    :param target:
    :return:
    """
    result = re.sub(r"\D", "", target)

    return result


def encrypt(message):
    PASS = os.getenv('PASS')
    SALT = os.getenv('SALT')
    ITER = os.getenv('ITER')
    DKEY = os.getenv('DKEY')
    private_key = hashlib.pbkdf2_hmac('SHA1', PASS.encode(), SALT.encode(), int(ITER), int(DKEY))
    message = pad(message.encode(), AES.block_size)
    iv = SALT
    cipher = AES.new(private_key, AES.MODE_CBC, iv.encode())
    return base64.b64encode(cipher.encrypt(message))

def generate_payload(id: str = "") -> str:
    """
    Generate payload for generate JEPFast QR code

    :param id: JEPFast id
    :return:
    """
    # sanitize id
    target = sanitize_target(id)
    encr = encrypt(target)
    total = encrypt(encr.decode() + SEPARATOR + ID_METHOD)
    return total.decode()


def to_image(payload: str = "") -> Image:
    """
    todo complete docblockr

    :param payload: JEPFast Payload
    :return:
    """
    img = qrcode.make(payload)

    return img


def to_file(payload: str = "", filepath: str = "") -> None:
    """

    :param payload: JEPFast Payload
    :param filepath: Target destination file path
    :return:
    """
    imgfile = open(filepath, "wb")
    img = to_image(payload)
    img.save(imgfile, "PNG")
    imgfile.close()


def print_tty(payload: str = "") -> None:
    """
    Output the QR Code only using TTY colors.

    :param payload: JEPFast Payload
    :return:
    """
    qr = qrcode.QRCode()
    qr.add_data(payload)
    qr.make()
    qr.print_tty()

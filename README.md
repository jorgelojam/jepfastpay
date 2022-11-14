# JEPFastPay

Python library to generate JEPFast QR Code for payments

## Installation

```
git clone https://github.com/jorgelojam/jepfastpay
cd jepfastpay
python setup.py install
```

## Usage

You must set enviroment variables for PASS, SALT, ITER, DKEY for your enviroment

### Library

```python
from jepfastpay import qrcode

# generate a payload
id_account = "0102030405"
payload = qrcode.generate_payload(id_account)
payload_with_token = qrcode.generate_payload(id_account)

# export to PIL image
img = qrcode.to_image(payload)

# export to file
qrcode.to_file(payload, "./qrcode-0102030405.png")
qrcode.to_file(payload_with_token, "/tmp/qrcode-0102030405.png") 
```

### CLI

```bash
python -m jepfastpay qrcode --id="0102030405"
python -m jepfastpay qrcode --id="0102030405" --file="./qrcode-cli.png"
python -m jepfastpay qrcode --id="0102030405" --show=true
python -m jepfastpay qrcode --id="0102030405" --file="/tmp/qrcode-cli-with-token.png"
```
import sys
from jepfastpay import qrcode

USAGE = """jepfastpay
Usage:
------
    $ jepfastpay qrcode --id="0102030405"
    $ jepfastpay qrcode --id="0102030405" --file="./qrcode-cli.png"
    $ jepfastpay qrcode --id="0102030405" --show=true
    $ jepfastpay qrcode --id="0102030405" --file="/tmp/qrcode-cli-with-token.png"

Available options are:
    -h, --help         Show this help
"""


def main():
    if sys.argv[1] == "qrcode" and len(sys.argv) > 2:
        args = sys.argv[2:]

        id_account = None
        filepath = None
        token = None
        is_show = False

        # parsing
        for arg in args:
            if arg.startswith("--id"):
                id_account = str(arg.split("=", 1)[1])
            elif arg.startswith("--file"):
                filepath = str(arg.split("=", 1)[1])
            elif arg.startswith("--show"):
                is_show = str(arg.split("=", 1)[1]).lower() == 'true'
            else:
                print("you are passing invalid argument", arg)
                sys.exit(0)

        if id_account:
            payload = qrcode.generate_payload(id_account)
            print("payload of %s: %s" % (id_account, payload))
            if filepath:
                qrcode.to_file(payload, filepath)
            if is_show:
                if sys.stdout.isatty():
                    qrcode.print_tty(payload)
                else:
                    img = qrcode.to_image(payload)
                    img.show()

    else:
        print(USAGE)
        sys.exit(0)


if __name__ == "__main__":
    main()

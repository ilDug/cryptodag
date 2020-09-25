from pathlib import Path
from source.install import Installer


class Importer():
    help_msg = """
Comandi disponibili:
    import-ca <ca_cert_path> <ca_key_path>   importa un certificato, la sua chiave privata
    """

    def __init__(self, args):
        # nessun comando
        if len(args) == 0:
            print(self.help_msg)
# _______________________________________________________________________________________________
        elif args[0] == "import-ca":
            if len(args) < 2:
                print("inserire il percorso al certificato della CA")
                print(self.help_msg)
                return
            if len(args) < 3:
                print("inserire il percorso della chiave privata della CA")
                print(self.help_msg)
                return

            cert_path = args[1]
            key_path = args[2]

            self.cert_file = Path(cert_path)
            self.key_file = Path(key_path)

            if not self.cert_file.exists():
                print("non è stato trovato il file del certificato")
                return

            if not self.key_file.exists():
                print("non è stato trovato il file della chiave privata")
                return

            i = Installer()
            i.clean_structure()
            i.create_pki()
            i.save_passphrase()

            cakey = Path(i.pki/'private/ca.key')
            cacrt = Path(i.pki/'certs/ca.crt')

            cakey.write_text(self.key_file.read_text())
            cacrt.write_text(self.cert_file.read_text())
# _______________________________________________________________________________________________
        else:
            print(self.help_msg)

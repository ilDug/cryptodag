from pathlib import Path
import os


class Cript():
    help_msg = """Comandi disponibili:
    cript (subject) (filename): restituisce la chiave pubblica
"""

    def __init__(self, subject):
        self.name = subject

################################################################################################

    def public_key(self, name, opts=[]):
        crt = Path('pki/certs/'+name+'.crt')
        if not crt.exists():
            print(
                "attenzione,  non esiste un certificato per il soggetto indicato " + name)
            return
        pubk = Path('pki/public/'+name+'.pub.pem')
        cmd = "openssl x509 \
            -pubkey \
            -noout \
            -in "+str(crt)+" \
            -out " + str(pubk)
        os.system(cmd)
        print(pubk.read_text())
        return pubk.read_text()

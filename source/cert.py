from pathlib import Path
import os


class Certificate():
    help_msg = """
    Comandi disponibili:
    pubkey:         restituisce la chiave pubblica
    verify-cert <path-to-cert>:    verifica che un certificato sia stato firmato dalla CA
"""

    def __init__(self, args):
        self.pki = Path('./pki')

        # nessun comando
        if len(args) == 0:
            print(self.help_msg)
# _______________________________________________________________________________________________
        elif args[0] == "pubkey":
            if len(args) < 2:
                print("inserire il nome del soggetto")
                return
            name,  *opts = args[1:]
            self.public_key(name, opts)
# _______________________________________________________________________________________________
        elif args[0] == "verify-cert":
            if len(args) < 2:
                print("inserire il percorso del certificato")
                return
            path = args[1]
            self.verifiy_cert(path)
# _______________________________________________________________________________________________
        else:
            print(self.help_msg)

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
################################################################################################

    def verifiy_cert(self, cert_path):
        cert = Path(cert_path)
        if not cert.exists():
            print("il certificato non esiste. controllare il percorso")
            return
        cacrt = Path(self.pki/'certs/ca.crt')
        print("\nVerifica certificato....")
        os.system("openssl verify -CAfile "+str(cacrt)+" " + str(cert))

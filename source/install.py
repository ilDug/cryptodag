from pathlib import Path
import shutil
import os
from getpass import getpass

#################################################
# cancella tutto quello che c'e\' nella directori pki
# crea una struttura di file e cartelle iniziale usando le impostazioni classiche
# genera una chiave per la CA
#################################################


class Installer():
    def __init__(self):
        self.pki = Path('./pki')
        self.dirs = ['certs', 'crl', 'newcerts',
                     'private', 'reqs', 'configs', 'public', 'workshop']
        self.conf_default = Path('source/openssl.cnf')
        self.conf_file = Path(self.pki/'configs/openssl.cnf')


######################################################################################

    def install(self):
        # controlla che la directory esista
        _continue = "y"
        if self.pki.exists():
            _continue = input(
                "l'infrastruttura e\' gia\' stata inizializzata. Se si prosegue tutti i dati verranno cancellati. Continuare [y/n]  ")
        if _continue == "y":
            installation_msg = """
- cancella tutto quello che c'e\' nella directori pki
- crea una struttura di file e cartelle iniziale usando le impostazioni classiche
- genera una chiave per la CA
            """
            print(installation_msg)
            self.clean_structure()
            self.create_pki()
            self.save_passphrase()
            self.create_ca_key()
            self.create_ca_crt()
            self.generate_public_key()


######################################################################################
    # pulisce la cartella della PKI

    def clean_structure(self):
        if self.pki.exists():
            shutil.rmtree('pki', ignore_errors=True)


######################################################################################

    def create_pki(self):
        #     mkdir certs crl newcerts private reqs configs && \
        #         chmod 700 private && \
        #         touch index.txt openssl.cnf && \
        #         echo 1000 > serial && \
        #         echo 1000 > crlnumber

        self.pki.mkdir(700)

        for p in [self.pki/Path(d) for d in self.dirs]:
            p.mkdir(700)

        Path(self.pki/'index.txt').write_text('')
        Path(self.pki/'serial').write_text('1000')
        Path(self.pki/'crlnumber').write_text('1000')

        # compila i file di opzioni
        with open(self.conf_default) as cdefault:
            with open(self.conf_file, 'w') as cfile:
                for line in cdefault:
                    cfile.write(line.replace('__pki_dir__', str(self.pki)))


######################################################################################

    def save_passphrase(self):
        while True:
            pw = getpass(
                "digitare la passphrase per la CERTIFICATE AUTHORITY: ")

            if not pw or len(pw) < 6:
                print("la passphrase deve avere almento 6 caratteri\n")
                continue
            break
        passphrase = Path(self.pki/'private/_passphrase')
        passphrase.write_text(pw)
        passphrase.chmod(400)


######################################################################################

    def create_ca_key(self):
        cakey = Path(self.pki/'private/ca.key')
        passphrase = Path(self.pki/'private/_passphrase')
        cakey = Path(self.pki/'private/ca.key')
        cmd = "openssl genrsa -aes256 -passout file:" + \
            str(passphrase) + " -out " + \
            str(cakey) + " 4096"
        os.system(cmd)
        cakey.chmod(400)


######################################################################################

    def create_ca_crt(self):
        # config = Path('pki/configs/openssl.cnf')
        passphrase = Path(self.pki/'private/_passphrase')
        cakey = Path(self.pki/'private/ca.key')
        cacrt = Path(self.pki/'certs/ca.crt')

        cmd = "openssl req \
        -x509 -new -nodes -sha256 -verbose \
        -days 365 \
        -passin file:" + str(passphrase) + " \
        -key " + str(cakey) + "   \
        -out " + str(cacrt)
        # cmd = "openssl req \ -config " + str(config) + " \ -extensions v3_ca \ -x509 -new -nodes -sha256 -verbose \ -days 1825 \ -passin file:" + str(passphrase) + " \ -key " + str(cakey) + "   \ -out " + str(cacrt)
        os.system(cmd)
        cacrt.chmod(444)


######################################################################################

    def generate_public_key(self):
        cacrt = Path(self.pki/'certs/ca.crt')
        pubkey = Path(self.pki/"public/ca.pub.pem")
        cmd = "openssl x509 \
        -pubkey \
        -noout \
        -in " + str(cacrt) + " \
        -out " + str(pubkey)
        os.system(cmd)

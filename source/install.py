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
        # controlla che la directory esista
        self.pki = Path('./pki')
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
            self.create_pki()
            self.create_ca_key()
            self.create_ca_crt()
            self.generate_public_key()

    def create_pki(self):
        #     mkdir certs crl newcerts private reqs configs && \
        #         chmod 700 private && \
        #         touch index.txt openssl.cnf && \
        #         echo 1000 > serial && \
        #         echo 1000 > crlnumber

        pki = Path('pki')
        if pki.exists():
            shutil.rmtree('pki', ignore_errors=True)
        pki.mkdir(700)

        dirs = ['certs', 'crl', 'newcerts',
                'private', 'reqs', 'configs', 'public', 'workshop']

        for p in [pki/Path(d) for d in dirs]:
            p.mkdir(700)

        Path(pki/'index.txt').write_text('')
        Path(pki/'serial').write_text('1000')
        Path(pki/'crlnumber').write_text('1000')

        conf_default = Path('source/openssl.cnf')
        conf_file = Path('pki/configs/openssl.cnf')
        # conf_content = conf_default.read_text()
        # conf_file.write_text(conf_content)
        with open(conf_default) as cdefault:
            with open(conf_file, 'w') as cfile:
                for line in cdefault:
                    cfile.write(line.replace('__pki_dir__', str(pki)))

        # shutil.copy(Path('source/openssl.cnf'), str(pki/'configs'))

        pw = getpass("digitare la passphrase per la CERTIFICATE AUTHORITY: ")

        passphrase = Path(pki/'private/_passphrase')
        passphrase.write_text(pw)
        passphrase.chmod(400)

        # with open(Path(pki/'index.txt'), 'w') as f:
        #     pass

    def create_ca_key(self):
        passphrase = Path('pki/private/_passphrase')
        cakey = Path('pki/private/ca.key')
        cmd = "openssl genrsa -aes256 -passout file:" + \
            str(passphrase) + " -out " + \
            str(cakey) + " 4096"
        os.system(cmd)
        cakey.chmod(400)

    def create_ca_crt(self):
        # config = Path('pki/configs/openssl.cnf')
        passphrase = Path('pki/private/_passphrase')
        cakey = Path('pki/private/ca.key')
        cacrt = Path('pki/certs/ca.crt')

        cmd = "openssl req \
        -x509 -new -nodes -sha256 -verbose \
        -days 3650 \
        -passin file:" + str(passphrase) + " \
        -key " + str(cakey) + "   \
        -out " + str(cacrt)
        # cmd = "openssl req \ -config " + str(config) + " \ -extensions v3_ca \ -x509 -new -nodes -sha256 -verbose \ -days 3650 \ -passin file:" + str(passphrase) + " \ -key " + str(cakey) + "   \ -out " + str(cacrt)
        os.system(cmd)
        cacrt.chmod(444)

    def generate_public_key(self):
        cacrt = Path('pki/certs/ca.crt')
        pubkey = Path("pki/public/ca.pub.pem")
        cmd = "openssl x509 \
        -pubkey \
        -noout \
        -in " + str(cacrt) + " \
        -out " + str(pubkey)
        os.system(cmd)

import sys
import os
import shutil
from pathlib import Path
from string import Template


class Gen():
    help_msg = """
Comandi disponibili:
    privkey (subject) [bit]:            genera una chiave privata con il nome subject (opzionale il numero di bit = 2048)
    req (subject) [alt-names, ...]:     genera una richiestadi firma per un certificato
    cert (subject) [alt_names]:         genera un certificato firmato da CA
"""

    def __init__(self, args):
        self.pki = Path('./pki')

        # nessun comando
        if len(args) == 0:
            print(self.help_msg)
# _______________________________________________________________________________________________
        elif args[0] == "privkey":
            if len(args) < 2:
                print("inserire il nome del soggetto")
                return
            name = args[1]
            self.gen_privkey(name)
# _______________________________________________________________________________________________
        elif args[0] == "req":
            if len(args) < 2:
                print("inserire il nome del soggetto")
                return
            name, *alt_names = args[1:]
            self.gen_config(name, alt_names)
            self.gen_req(name)
# _______________________________________________________________________________________________
        elif args[0] == "cert":
            if len(args) < 2:
                print(
                    "inserire il nome del soggetto ed eventuali alternative names per DNS")
                return
            name, *alt_names = args[1:]
            self.gen_privkey(name)
            self.gen_config(name, alt_names)
            self.gen_req(name)
            self.gen_cert(name)
# _______________________________________________________________________________________________
        else:
            print(self.help_msg)
######################################################################################

    def gen_privkey(self, name, bits=2048):
        key = Path(str(self.pki) + '/private/' + name + '.key')
        cmd = "openssl genrsa -out " + str(key) + " " + str(bits)
        os.system(cmd)
######################################################################################

    def gen_req(self, name):
        key = Path(str(self.pki) + '/private/' + name + '.key')
        csr = Path(str(self.pki) + '/reqs/' + name + '.csr')
        config = Path(str(self.pki) + '/configs/' + name + '.cnf')

        cmd = 'openssl req \
            -config ' + str(config) + ' \
            -new -sha256 -verbose -batch \
            -key ' + str(key) + ' \
            -out ' + str(csr)

        os.system(cmd)
        os.system("openssl req -text -noout -in " + str(csr))
######################################################################################

    def gen_config(self, name, alt_names):
        default = Path('source/default.cnf')
        config = Path(str(self.pki) + '/configs/' + name + '.cnf')
        extensions = [
            "subjectAltName = @alt_names\n",
            "[alt_names]\n",
            "DNS." + str(len(alt_names)+1) + " = " + name + "\n"
        ]

        for i in range(len(alt_names)):
            s = "DNS." + str(i+1) + " = " + alt_names[i] + "\n"
            extensions.append(s)

        with open(default) as old:
            with open(config, 'w') as new:
                for line in old:
                    new.write(line.replace('__subject__', name))
                if len(alt_names) > 0:
                    new.writelines(extensions)
######################################################################################

    def gen_cert(self, name):
        config = Path(self.pki/'configs/openssl.cnf')
        extfile = Path(str(self.pki) + '/configs/' + name + '.cnf')
        pw = Path(self.pki/'private/_passphrase')
        csr = Path(str(self.pki) + '/reqs/' + name + '.csr')
        crt = Path(str(self.pki) + '/certs/' + name + '.crt')
        cacrt = Path(self.pki/'certs/ca.crt')
        cmd = 'openssl ca \
            -config ' + str(config) + ' \
            -notext -md sha256 -days 365 -verbose -batch\
            -extfile ' + str(extfile) + ' \
            -extensions req_ext \
            -passin file:' + str(pw) + ' \
            -in ' + str(csr) + ' \
            -out ' + str(crt)
        os.system(cmd)
        print("\n\n\n************************\ncertificato generato\n************************\n\n")
        os.system("openssl x509 -noout -text -in " + str(crt))
        print("\nVerifica certificato;")
        os.system("openssl verify -CAfile "+str(cacrt)+" " + str(crt))

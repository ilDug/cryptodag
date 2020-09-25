import sys
from pathlib import Path
from source.gen import Gen
from source.cript import Cript
from source.cert import Certificate
from source.install import Installer
from source.importer import Importer

args = sys.argv
del args[0]

help_message = """
Comandi disponibili:
    install:    genera tutta l'infrastruttira della PKI compreso il certificato root
    import-ca:  genera tutta l'infrastruttira della PKI importando la chiave ed il certificato root
    gen:        genera un elemento(vedi opzioni),
    pubkey:     restituisce la chiave pubblica
    sign:       firma un file
    verify-sign:     verifica la firma
    verify-cert:     verifica un certificato
    crypt:      cripta un file
    decript:    decripta un file
    """

# controlla che sia installato il sistema di CA
cwd = Path('./pki')


# decide quale comando utilizzare

# nessun comando
if len(args) == 0:
    print(help_message)

elif args[0] == "install":
    i = Installer()
    i.install()

elif cwd.exists() == False:
    print("prima di utilizzare il programma esegui l'inizializzazione con il comando 'install' ")
    sys.exit()

elif args[0] == "gen":
    gen = Gen(args[1:])

elif args[0] == "pubkey":
    cert = Certificate(args)


elif args[0] == "import-ca":
    i = Importer(args)

elif args[0] == "verify-cert":
    c = Certificate(args)

elif args[0] == "cript":
    pass

else:
    print(help_message)

sys.exit()

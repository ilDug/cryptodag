import sys
from pathlib import Path
from source.gen import Gen
from source.cript import Cript
from source.cert import Certificate
from source.install import Installer

args = sys.argv
del args[0]

help_message = """
Comandi disponibili:
    install:    genera tutta l'infrastruttira ella PKI compreso il certificato root
    gen:        genera un elemento(vedi opzioni),
    pubkey:     restituisce la chiave pubblica
    sign:       firma un file
    verify:     verifica la firma
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

elif cwd.exists() == False:
    print("prima di utilizzare il programma esegui l'inizializzazione con il comando 'install' ")
    sys.exit()

elif args[0] == "gen":
    gen = Gen(args[1:])

elif args[0] == "pubkey":
    cert = Certificate(args)

elif args[0] == "cript":
    pass

else:
    print(help_message)

sys.exit()

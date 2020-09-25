from pathlib import Path
import os


class Crypt():
    help_msg = """
Comandi disponibili:
    crypt sym <filein> 
    crypt asym <filein>  <subject>
"""

    def __init__(self, args):
        # nessun comando
        if len(args) == 0:
            print(self.help_msg)
# _______________________________________________________________________________________________
        elif args[0] == "sym":
            if len(args) < 2:
                print("inserire il nome del file da criptare")
                return
            self.file,  *self.opts = args[1:]
            self.crypt_sym()
# _______________________________________________________________________________________________
        # elif args[0] == "asym":
        #     if len(args) < 2:
        #         print("inserire il nome del file da criptare")
        #         return
        #     if len(args) < 3:
        #         print(
        #             "inserire il nome del soggetto che possiede certificato salvato nell PKI")
        #         return
        #     file_in, subject = args[1:]
        #     self.crypt_asym(file_in, subject)
# _______________________________________________________________________________________________
        else:
            print(self.help_msg)

################################################################################################
    def crypt_sym(self):
        source = Path(self.file)
        pw = str(source) + '.pw'
        dest = str(source) + '.crypt'
        cmd = f"openssl rand -hex -out '{pw}' 64"
        os.system(cmd)

        cmd = f"openssl enc -aes256 -salt -e -a \
            -pass file:'{pw}' \
            -in '{str(source)}' \
            -out '{dest}'"
        os.system(cmd)

################################################################################################
    # def crypt_asym(self, file_in, subject):
    #     source = Path(file_in)
    #     cert = Path('pki/certs/' + subject + '.crt')
    #     dest = str(source) + '.crypt'

    #     cmd = f"openssl rsautl -encrypt -certin \
    #         -inkey '{str(cert)}' \
    #         -in '{str(source)}' \
    #         -out '{dest}'"
    #     os.system(cmd)

################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################


class Decrypt():
    help_msg = """
Comandi disponibili:
    decrypt sym <crypt_file> <password_file> 
"""

    def __init__(self, args):
        # nessun comando
        if len(args) == 0:
            print(self.help_msg)
# _______________________________________________________________________________________________
        elif args[0] == "sym":
            if len(args) < 2:
                print("inserire il nome del file da criptare")
                return
            if len(args) < 3:
                print("inserire il nome del file della password")
                return
            self.file, self.pw, *self.opts = args[1:]
            self.decrypt_sym()
# _______________________________________________________________________________________________
        else:
            print(self.help_msg)


################################################################################################

    def decrypt_sym(self):
        source = Path(self.file)
        pw = Path(self.pw)
        dest = str(source).replace('.crypt', "")

        cmd = f"openssl enc -aes256 -d -a \
            -pass file:'{str(pw)}' \
            -in '{str(source)}' \
            -out '{dest}'"
        os.system(cmd)

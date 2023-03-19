import time
from AES import encrypt, decrypt
import argparse


class FilesEncryptor:
    def __init__(self, name, output_name):
        self.key = None
        self.name = name
        self.output_name = output_name

    def set_key(self, key):
        self.key = key

    def generateFile(self):
        with open(self.name, 'rb') as f:
            f = bytes.hex(f.read())

        self.name = encrypt(self.name.encode('utf-8').hex(), self.key)
        enc = encrypt(f, self.key)

        with open(self.output_name, 'wb') as f:
            f.write(bytes.fromhex(self.name) + b'\n')
            f.write(bytes.fromhex(enc))


class FilesDecryptor:

    def __init__(self, name):
        self.key = None
        self.name = name

    def set_key(self, key):
        self.key = key

    def generateFile(self):
        with open(self.name, 'rb') as f:
            self.name = bytes.hex(f.readline())[:-2]
            f = bytes.hex(f.read())

        self.name = self.removeNullCharacters(decrypt(self.name, self.key))
        self.name = bytes.fromhex(self.name).decode('utf-8')
        self.name = self.name.split('.')
        self.name[0] = self.name[0] + '(1)'
        self.name = '.'.join(self.name)

        data = self.removeNullCharacters(decrypt(f, self.key))

        with open(self.name, 'wb') as f:
            f.write(bytes.fromhex(data))

    def removeNullCharacters(self, data):
        while data[-2:] == '00':
            data = data[:-2]
        return data


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--encrypt", help="Encrypt given file")
parser.add_argument("-d", "--decrypt", help="Decrypt given file")
parser.add_argument("-k", "--key", required=True)
parser.add_argument("-o", "--output")
args = parser.parse_args()

passed_args = True
output_name = args.output

if args.encrypt:
    if output_name is None:
        print('You need to enter -o [output filename]')
        passed_args = False
    else: file_manager = FilesEncryptor(args.encrypt, output_name)
elif args.decrypt:
    file_manager = FilesDecryptor(args.decrypt)
else:
    passed_args = False
    print("Please specify either -e or -d")

if passed_args:
    key = args.key
    valid = True
    if len(key) != 32 and len(key) != 64 and len(key) != 48:
        print("Key is not valid")
        valid = False

    try:
        int(key, 16)
    except ValueError:
        print("Key is not valid. Key must be 32, 64 or 48 hexadecimal characters.")
        valid = False

    if valid:
        file_manager.set_key(key)
        x1 = time.time()
        file_manager.generateFile()
        x2 = time.time()
        print(f"Finished successfully in {x2 - x1} seconds")

import time
from AES import encrypt, decrypt
import argparse


class FilesEncryptor:
    def __init__(self, name, output_name='enc'):
        self.key = None
        self.name = name
        self.output = output_name

    def set_output(self, output):
        self.output = output

    def set_key(self, key):
        self.key = key

    def generateFile(self):
        with open(self.name, 'rb') as f:
            f = bytes.hex(f.read())

        self.name = encrypt(self.name.encode('utf-8').hex(), self.key)
        enc = encrypt(f, self.key)

        with open(self.output, 'wb') as f:
            f.write(bytes.fromhex(self.name) + b'\n')
            f.write(bytes.fromhex(enc))


class FilesDecryptor:
    def __init__(self, name, output_name=None):
        self.key = None
        self.name = name
        self.output = output_name

    def set_key(self, key):
        self.key = key

    def set_output(self, output):
        self.output = output

    def generateFile(self):
        with open(self.name, 'rb') as f:
            self.name = bytes.hex(f.readline())[:-2]
            f = bytes.hex(f.read())

        if self.output is None:
            self.output = self.removeNullCharacters(decrypt(self.name, self.key))
            self.output = bytes.fromhex(self.output).decode('utf-8')
            self.output = self.output.split('.')
            self.output[0] = self.output[0] + '(1)'
            self.output = '.'.join(self.output)

        data = self.removeNullCharacters(decrypt(f, self.key))

        with open(self.output, 'wb') as f:
            f.write(bytes.fromhex(data))

    def removeNullCharacters(self, data):
        while data[-2:] == '00':
            data = data[:-2]
        return data


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--encrypt", help="encrypt given file")
parser.add_argument("-d", "--decrypt", help="decrypt given file")
parser.add_argument("-k", "--key", required=True, help="key for encryption/decryption")
parser.add_argument("-o", "--output", help="name of output file")
args = parser.parse_args()

passed_args = True
if args.encrypt:
    file_manager = FilesEncryptor(args.encrypt)
elif args.decrypt:
    file_manager = FilesDecryptor(args.decrypt)
else:
    passed_args = False
    print("Please specify either -e or -d")

if passed_args:
    if args.output is not None: file_manager.set_output(args.output)

    key = args.key
    try:
        int(key, 16)
    except ValueError:
        print("Key is not valid. Key must be 32, 64 or 48 hexadecimal characters.")
        valid = False

    valid = True
    if len(key) != 32 and len(key) != 64 and len(key) != 48:
        print("Key is not valid")
        valid = False

    if valid:
        file_manager.set_key(key)
        x1 = time.time()
        file_manager.generateFile()
        x2 = time.time()
        print(f"Finished successfully in {x2 - x1} seconds")

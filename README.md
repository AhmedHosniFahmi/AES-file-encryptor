# AES-files-Encryptor-Decryptor
A script that encrypts & decrypts files using AES-128-ECB, AES-192-ECB or AES-256-ECB algorithms.

## Features
This script provides the following features:

- 128 bit keys
- 192 bit keys
- 256 bit keys
- ECB Mode

## Usage

Here is how to run the files encryptor & decryptor from the CLI:

````bash
usage: files_encryptor_decryptor.py [-h] [-e ENCRYPT] [-d DECRYPT] -k KEY [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -e ENCRYPT, --encrypt ENCRYPT
                        encrypt given file
  -d DECRYPT, --decrypt DECRYPT
                        decrypt given file
  -k KEY, --key KEY     key for encryption/decryption, must be 32, 64 or 48 hexadecimal characters.
  -o OUTPUT, --output OUTPUT
                        name of output file
````
For example: to encrypt the file `some_file.pdf`:
````bash
./files_encryptor_decryptor.py -e some_file.pdf -k 4d6f68616d6564204d6f6174617a202020204d6f68616d6564204d6f6174617a
````
A file named `enc` is generated because no output file name was passed.

And to decrypt the `enc` file:
````bash
./files_encryptor_decryptor.py -d enc -k 4d6f68616d6564204d6f6174617a202020204d6f68616d6564204d6f6174617a  -o same_old_file.pdf
````
`same_old_file.pdf` is generated which is the same as `some_file.pdf`

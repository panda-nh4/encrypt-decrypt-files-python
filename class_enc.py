from cryptography.fernet import Fernet


class Encryptor:
    def decrypt_fname(self, key, fname):
        f = Fernet(key)
        decrypted = f.decrypt(fname)
        output = str(decrypted, "UTF-8")
        return output

    def encrypt_fname(self, key, fname):
        f = Fernet(key)
        encrypted = f.encrypt(bytes(fname, "utf-8"))
        return str(encrypted, "UTF-8")

    def key_create(self, key_name):
        key = Fernet.generate_key()
        with open(key_name, "wb") as mykey:
            mykey.write(key)
        return key

    def file_encrypt(self, key, original_file, encrypted_file):
        f = Fernet(key)

        with open(original_file, "rb") as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open(encrypted_file, "wb") as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file, decrypted_file):
        f = Fernet(key)

        with open(encrypted_file, "rb") as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, "wb") as file:
            file.write(decrypted)

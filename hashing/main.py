from hashing.src.Hash import HashHelper
from hashing.src.DatabaseController import DatabaseController
from hashing.src.Transfer import Transfer
from getpass import getpass

if __name__ == '__main__':
    # HashHelper.hashing_time_for_all_algorithms(text='password', loops=10000)
    # name = Transfer.download_file("https://releases.ubuntu.com/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso")
    # HashHelper.compare_file_with_checksum("./{}".format(name), "93bdab204067321ff131f560879db46bee3b994bf24836bb78538640f689e58f", "sha256")
    # HashHelper.display_plot(
    #    HashHelper.generate_hash_size_times(length=1000000, algorithm="sha1", step=100000, loops=1000))

    username = input("Username: ")
    password = input("Password: ")  # getpass("Password:")
    password2 = input("Repeat Password: ")  # getpass("Repeat Password:")
    if password == password2:
        algorithm = None
        while algorithm is None:
            print("Please enter number of your prefered algorithm 1. SHA512 2. pbkdf2_hmac")
            prefered = int(input())
            if prefered == 1:
                algorithm = "SHA512"
            elif prefered == 2:
                algorithm = "PBKDF2_HMAC"
            else:
                print("Number not recognized please try again.")
        salt = HashHelper.generate_salt()
        password = HashHelper.hash_password(password, salt, algorithm)
        print(password)
        db = DatabaseController('./clients')
        db.create_user(username, password, salt, algorithm)
        print(HashHelper.verify_password('./clients', 'adasumizox', password))

    else:
        print("Passwords are not the same")
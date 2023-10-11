import math
import os
import sys
from class_enc import Encryptor
import shutil
from filesplit.split import Split
from filesplit.merge import Merge


def make_key(kname):
    try:
        Encryptor().key_create(kname)
    except Exception as e:
        print(e)


def scorched_earth():
    path = os.getcwd()
    shutil.rmtree(path)


def view_del(source_path):
    f = []
    if os.path.isdir(source_path):
        for dirpath, dirnames, filenames in os.walk(source_path):
            f.extend(filenames)
            break
        tot_files = len(f)
        err_f_count = 0
        for file in f:
            try:
                os.remove(os.path.join(source_path, file))
            except:
                err_f_count += 1
                print("Unable to delete file " + file)
        print(
            "Deleted "
            + str(tot_files - err_f_count)
            + " of "
            + str(tot_files)
            + " files."
        )


def mergeAndDecrypt(container_dir,dest_path,key_path,dir_name):
    temp_path=os.path.join(os.getcwd(),"temp")
    os.mkdir(temp_path)
    enc_obj = Encryptor()
    with open(key_path, "rb") as mykey:
        key = mykey.read()
    new_fname = enc_obj.decrypt_fname(key,dir_name[4:])
    decrypt_files(container_dir,temp_path,key_path)
    merge = Merge(temp_path, dest_path, new_fname)
    merge.merge()
    shutil.rmtree(temp_path)


def decrypt_files(source_path, dest_path, key_path):
    f = []
    fd=[]
    if os.path.isdir(source_path) and os.path.isdir(dest_path):
        if os.path.isfile(key_path):
            for dirpath, dirnames, filenames in os.walk(source_path):
                f.extend(filenames)
                fd.extend(dirnames)
                break
            with open(key_path, "rb") as mykey:
                key = mykey.read()
            # print(f)
            tot_files = len(f)
            files_encp = 0
            enc_error_count = 0
            enc_err_lst = []
            enc_obj = Encryptor()
            for dir in fd:
                try:
                    if "Part" in dir:
                        print("Split file found!")
                        tot_files+=1
                        print("++++++++Subfiles++++++++")
                        mergeAndDecrypt(os.path.join(source_path,dir),dest_path,key_path,dir)
                        print("++++++++++++++++++++++++")
                        files_encp += 1
                except Exception as e:
                    enc_error_count += 1
                    enc_err_lst.append(dir)
                    print("Error: "+dir)
                    print(e)

            for file in f:
                try:
                    new_fname = enc_obj.decrypt_fname(key, file)
                    enc_obj.file_decrypt(
                        key,
                        os.path.join(source_path, file),
                        os.path.join(dest_path, new_fname),
                    )
                    files_encp += 1
                except Exception as e:
                    enc_error_count += 1
                    enc_err_lst.append(file)
                    print("Error: "+file+" not decrypted")
                    print(e)
            print("Decrypted " + str(files_encp) + " of " + str(tot_files) + " files!")
            print(str(enc_error_count) + " files not decrypted.")
        else:
            print("Key not found!")
    else:
        print("Directory does not exist!")


def encrypt_files(source_path, dest_path, key_path):
    f = []
    if os.path.isdir(source_path) and os.path.isdir(dest_path):
        if os.path.isfile(key_path):
            for dirpath, dirnames, filenames in os.walk(source_path):
                f.extend(filenames)
                break
            with open(key_path, "rb") as mykey:
                key = mykey.read()
            # print(f)
            tot_files = len(f)
            files_encp = 0
            enc_error_count = 0
            enc_err_lst = []
            enc_obj = Encryptor()
            max_size=400000000
            for file in f:
                try:
                    f_size=os.path.getsize(os.path.join(source_path, file))
                    if f_size>max_size:
                        print(file+" is too large. Splitting!")
                        print("++++++++Subfiles++++++++")
                        new_fname = enc_obj.encrypt_fname(key, file)
                        new_fname="Part"+new_fname
                        new_path=os.path.join(dest_path,new_fname)
                        os.mkdir(new_path)
                        split = Split(os.path.join(source_path, file),new_path)
                        split.bysize(max_size)
                        encrypt_files(new_path,new_path,key_path)
                        print("++++++++++++++++++++++++")
                        num_f=[]
                        for dirpath, dirnames, filenames in os.walk(new_path):
                            num_f.extend(filenames)
                            break
                        if len(num_f)!=((math.ceil(f_size/max_size)+1)):
                            raise Exception("Splitting unsuccessful")



                    else:
                        new_fname = enc_obj.encrypt_fname(key, file)
                        enc_obj.file_encrypt(
                            key,
                            os.path.join(source_path, file),
                            os.path.join(dest_path, new_fname),
                        )
                    files_encp += 1
                except Exception as e:
                    enc_error_count += 1
                    enc_err_lst.append(file)
                    print("b1")
                    print(e)

            fi = []
            for dirpath, dirnames, filenames in os.walk(source_path):
                fi.extend(filenames)
                break
            for file in fi:
                if file in enc_err_lst or file not in f:
                    continue
                try:
                    os.remove(os.path.join(source_path, file))
                except:
                    print("Unable to delete file " + file)
            print("Encrypted " + str(files_encp) + " of " + str(tot_files) + " files!")
            print(str(enc_error_count) + " files not encrypted.")

            pass
        else:
            print("Key not found!")
    else:
        print("Directory does not exist!")


if __name__ == "__main__":
    decrypt_files_path = os.getcwd() + os.sep + "to_encrypt" + os.sep
    encrypt_files_path = os.getcwd() + os.sep + "files_encrypted" + os.sep
    view_files_path = os.getcwd() + os.sep + "view" + os.sep
    key = os.getcwd() + os.sep + "key1"
    try:
        if not os.path.isdir(decrypt_files_path):
            os.mkdir(decrypt_files_path)
        if not os.path.isdir(encrypt_files_path):
            os.mkdir(encrypt_files_path)
        if not os.path.isdir(view_files_path):
            os.mkdir(view_files_path)

        # For auto-complete. Yeah yeah its a crappy way.
        # Well im lazy.
        auto_keys=['help','make_key','encrypt','decrypt','delete','scorched_earth']
        for _ in auto_keys:
            if not os.path.isfile(os.getcwd()+os.sep+_):
                f = open(os.getcwd()+os.sep+_, "x")

    except:
        print("Error creating default directories.")
    if len(sys.argv) == 1:
        print("Need args.\nTry '" + sys.argv[0] + " help'")
        exit()
    if sys.argv[1].lower() == "scorched_earth":
        scorched_earth()
        exit()
    if sys.argv[1].lower() == "help":
        print("\nTo create a new key : [script_name] make_key path_to_key")
        print(
            "To encrypt and delete original files : [script_name] encrypt source_dir_path dest_dir_path path_to_key"
        )
        print(
            "To decrypt and view files : [script_name] decrypt source_dir_path dest_dir_path path_to_key"
        )
        print(
            "To delete files in view directory : [script_name] delete path_to_view_dir"
        )
        print(
            "To delete everything in directory of script : [script_name] scorched_earth"
        )
        print("\nDefault values :")
        print("path_to_key : " + key)
        print("Path to files to be encrypted : " + decrypt_files_path)
        print("Path to encrypted files : " + encrypt_files_path)
        print("Path to view directory : " + view_files_path)
    elif sys.argv[1].lower() == "make_key" and (
        len(sys.argv) == 3 or len(sys.argv) == 2
    ):
        if len(sys.argv) == 3:
            key = sys.argv[2]
        make_key(key)
    elif sys.argv[1].lower() == "encrypt" and (
        len(sys.argv) == 5 or len(sys.argv) == 2
    ):
        if len(sys.argv) == 5:
            decrypt_files_path = sys.argv[2]
            encrypt_files_path = sys.argv[3]
            key = sys.argv[4]
        encrypt_files(decrypt_files_path, encrypt_files_path, key)
    elif sys.argv[1].lower() == "decrypt" and (
        len(sys.argv) == 5 or len(sys.argv) == 2
    ):
        if len(sys.argv) == 5:
            encrypt_files_path = sys.argv[2]
            view_files_path = sys.argv[3]
            key = sys.argv[4]
        decrypt_files(encrypt_files_path, view_files_path, key)

    elif sys.argv[1].lower() == "delete" and (len(sys.argv) == 3 or len(sys.argv) == 2):
        if len(sys.argv) == 3:
            view_files_path = sys.argv[2]
        view_del(view_files_path)
    else:
        print("Incorrect args.\nTry '" + sys.argv[0] + " help'")

    exit()

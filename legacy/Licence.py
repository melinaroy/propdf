import ctypes
import os
import shutil

USER_FOLDER = os.path.join(os.environ["USERPROFILE"]) + "\\"
script_dir = os.path.dirname(os.path.abspath(__file__))
icon = "pro-pdf_icon.ico"
icon_source_path = os.path.join(script_dir, icon)
name = "sys.txt"
folder_appdata = "AppData"
folder_local = "Local"
folder_name = "zpkr-ojdam-ndakm-uooak"
directory_appdata = USER_FOLDER + folder_appdata
directory_local = directory_appdata + "\\" + folder_local
directory = directory_local + "\\" + folder_name
icon_path = directory + "\\" + icon
file_path = directory + "\\" + name
if os.path.isdir(directory):
    ctypes.windll.kernel32.SetFileAttributesW(directory, 2)
    if os.path.isfile(icon_path):
        if os.path.isfile(file_path):
            print("Licence déjà présente sur l'ordinateur.")
            print("...Terminé")
        else:
            with open(file_path, "w") as f:
                f.write("LICENCE")
            p = os.popen("attrib +h " + file_path)
            t = p.read()
            p.close()
            print("Licence installée.")
            print("...Terminé")
    else:
        shutil.copy(icon_source_path, directory)
        print("Icon installée.")
        if os.path.isfile(file_path):
            print("Licence déjà présente sur l'ordinateur.")
            print("...Terminé")
        else:
            with open(file_path, "w") as f:
                f.write("LICENCE")
            p = os.popen("attrib +h " + file_path)
            t = p.read()
            p.close()
            print("Licence installée.")
            print("...Terminé")
else:
    os.makedirs(directory)
    ctypes.windll.kernel32.SetFileAttributesW(directory_appdata, 2)
    ctypes.windll.kernel32.SetFileAttributesW(directory, 2)
    print("...Ok.")
    shutil.copy(icon_source_path, directory)
    print("...Ok.")
    with open(file_path, "w") as f:
        f.write("LICENCE")
    p = os.popen("attrib +h " + file_path)
    t = p.read()
    p.close()
    print("...Ok.")
    print("...Terminé")

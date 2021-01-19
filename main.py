import os
import paramiko



def download(ip, filename, remotepath, localpath=''):
    path = os.getcwd()
    if localpath != '':
        try:
            if not os.path.exists(path + localpath):
                os.makedirs(path + localpath)
        except OSError:
            print(f"Creation of the directory {path + localpath} failed")
        else:
            print(f"Directory {path + localpath}")
    else:
        localpath = '/'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username="root", password="strom")
    except Exception as e:
        print(e)
        print("It doesn't seem to be Prague's VM \nTrying to use RU credentials instead")
        ssh.connect(ip, username="dboriso", password="B52-a418-C949")
    sftp = ssh.open_sftp()
    sftp.get(remotepath + filename, path + localpath + filename,
             callback=lambda x, y: print(f'{filename} transferred: {x / y * 100:.0f}%'))
    sftp.close()
    ssh.close()


def upload(ip, filename, remotepath, localpath=''):
    path = os.getcwd()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username="root", password="strom")
    except Exception as e:
        print(e)
        print("It doesn't seem to be Prague's VM \nTrying to use RU credentials instead")
        ssh.connect(ip, username="dboriso", password="B52-a418-C949")
    sftp = ssh.open_sftp()
    try:
        sftp.chdir(remotepath)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remotepath)  # Create remote_path
        sftp.chdir(remotepath)
    sftp.put(localpath=path + localpath + filename, remotepath=remotepath + filename,
             callback=lambda x, y: print(f' transferred: {x / y * 100:.0f}%'))
    sftp.close()
    ssh.close()


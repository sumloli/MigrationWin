import os
import paramiko
import shutil



win_ips = ['10.240.206.114','10.240.206.115','10.240.206.116']
xmls = ['core_olm.xml', 'logging.xml', 'oam.xml']
lin_ip = '10.240.151.134'

def download_win_see_def_cfgs(source_ip, dest_path, file_name):
    shutil.copyfile(os.path.join(f'//{source_ip}/sts/see/defaultcfg', file_name), os.path.join(dest_path, file_name))


def download_win_see_actual_cfgs(source_ip, dest_path, file_name):
    shutil.copyfile(os.path.join(f'//{source_ip}/sts/see/', file_name), os.path.join(dest_path, file_name))


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory) # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        mkdir_p(sftp, dirname) # make parent directories
        sftp.mkdir(basename) # sub-directory missing, so created it
        sftp.chdir(basename)
        return True


def download_all():
    for ip in win_ips:
        os.makedirs(f'C:/opt/sts/Migration/see[{ip}]/defaultcfg', exist_ok=True)
        os.makedirs(f'C:/opt/sts/Migration/see[{ip}]/actualcfg', exist_ok=True)
        print(f'folder "see[{ip}]" is created')
        for xml in xmls:
            download_win_see_def_cfgs(ip, f'C:/opt/sts/Migration/see[{ip}]/defaultcfg', xml)
            print(f' -- "{xml}" is downloaded')
        for xml in xmls:
            try:
                download_win_see_actual_cfgs(ip, f'C:/opt/sts/Migration/see[{ip}]/actualcfg', xml)
                print(f' -- "{xml}" is downloaded')
            except:
                print(f' -- "{xml}" is not found')



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
        mkdir_p(sftp, remotepath)  # Create remote_path
        sftp.chdir(remotepath)
    sftp.put(localpath=os.path.join(localpath, filename), remotepath=os.path.join(remotepath, filename),
             callback=lambda x, y: print(f' transferred: {x / y * 100:.0f}%'))
    sftp.close()
    ssh.close()


def upload_all():
    for dir in os.listdir('C:/opt/sts/Migration/'):
        print(dir)
        for xml in os.listdir(f'C:/opt/sts/Migration/{dir}/defaultcfg'):
            print(xml)
            # print(os.path.join('c:' + os.sep, 'opt', 'sts', 'Migration', dir, 'defaultcfg', xml))
            print('to: ',  os.path.join(os.sep+'opt', 'sts', 'migration', 'Migration', 'platform', dir, 'defaultcfg'+os.sep).replace("\\", "/"))
            print('from: ', os.path.join('c:'+os.sep, 'opt', 'sts', 'Migration', dir, 'defaultcfg'+os.sep))
            try:
                upload(lin_ip, xml, os.path.join(os.sep+'opt', 'sts', 'migration', 'Migration', 'platform', dir, 'defaultcfg'+os.sep).replace("\\", "/"),
                       os.path.join('c:'+os.sep, 'opt', 'sts', 'Migration', dir, 'defaultcfg'+os.sep))
            except Exception as e:
                print("error here")
                print(e)
        for xml in os.listdir(f'C:/opt/sts/Migration/{dir}/actualcfg'):
            print(xml)
            print(os.path.join('c:' + os.sep, 'opt', 'sts', 'Migration', dir, 'actualcfg', xml))
            try:
                upload(lin_ip, xml, os.path.join(os.sep+'opt', 'sts', 'migration', 'Migration', 'platform', dir, 'actualcfg'+os.sep).replace("\\", "/"),
                       os.path.join('c:'+os.sep, 'opt', 'sts', 'Migration', dir, 'actualcfg'))
            except Exception as e:
                print("error here")
                print(e)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(lin_ip, username="root", password="strom")
    sftp = ssh.open_sftp()
    f = sftp.open('/opt/sts/migration/Migration/win.done', 'w')
    f.close()
    print('Upload finished, proceed at linux')

download_all()
upload_all()
input()
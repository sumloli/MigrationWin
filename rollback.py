import os
import shutil


def upload_win_see_actual_cfgs(dest_ip, source_path, file_name):
    shutil.copyfile(os.path.join(f'//{source_path}/sts/see/', file_name), os.path.join(dest_ip, file_name))


def rollback(platform):
    folders_list = [f for f in os.listdir(platform) if not f.startswith('.')]
    print(f'Starting rollback of {platform}')
    print(folders_list)
    for folder in folders_list:
        print(f'Module: {folder}')
        ip = folder.split('[')[1][:-1].upper()
        print(ip)
        for cfg in os.listdir(f'{platform}/{folder}/actualcfg'):
            print(cfg)
            if cfg == 'bus.ini':
                # editing bus ini and uploading it with new parameters back
                busini = f'{os.getcwd()}/{platform}/{folder}/actualcfg/bus.ini'
                print(busini)
                with open(busini, 'r') as f:
                    lines = f.readlines()
                    print(lines)
                with open(busini, 'w') as f:
                    for line in lines:
                        line = line.replace('newcm=true', 'newcm=false')
                        f.write(line)
                        print(line)
            upload_win_see_actual_cfgs(dest_ip=ip, source_path=f'C:/opt/sts/Migration/see[{ip}]/actualcfg',
                                       file_name=cfg)

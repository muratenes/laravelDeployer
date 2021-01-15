#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
from tempfile import mkstemp

from models.configs import SiteConfig, SshConfig, GeneralConfigs
from os import system
from os import fdopen, remove
from shutil import move


def createNginxFile(siteConfig, sshConfig, generalConfig):
    print("====== configuring to Nginx file =======")
    print("created => /etc/nginx/sites-available/%s" % siteConfig.site_folder_name)
    replaceText("scripts/nginxText", "site_folder", siteConfig.site_folder_name)
    replaceText("scripts/nginxText", "domain_name", siteConfig.domain_list)
    replaceText("scripts/nginxText", "parent_folder", generalConfig.sites_container_folder)
    with open('scripts/nginxText', 'r') as file:
        data = file.readlines()
        data.clear()


# bütün scriptleri varsayılan hale getirir
def setToDefaultScripts():
    print("====== configuring to Nginx file default settings =======")
    with open("scripts/defaultScripts/deleteOldDatasScript(Not Edit)") as f:
        lines = f.readlines()
        lines = [l for l in lines]
        with open("scripts/deleteOldDatasScript", "w") as f1:
            f1.writelines(lines)
    with open("scripts/defaultScripts/nginxText(Not edit)") as f:
        lines = f.readlines()
        lines = [l for l in lines]
        with open("scripts/nginxText", "w") as f1:
            f1.writelines(lines)


def pushToNginxFileToServer(siteConfig, sshConfig, generalConfig):
    system("ssh %s@%s 'bash -s' < 'scripts/nginxText'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("ssh %s@%s 'sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled'" % (
    SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))
    system("ssh %s@%s 'sudo systemctl restart nginx'" % (sshConfig.ssh_user, sshConfig.ssh_ip))


def replaceText(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
                print("[" + pattern + "] changed to ", "[", subst, "]")
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def index():
    pass


if __name__ == '__main__':
    index()

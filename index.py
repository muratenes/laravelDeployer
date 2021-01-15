import sys

from models.configs import SiteConfig, SshConfig, GeneralConfigs
from os import system
import laraConf
import privateConfigs


def bindSshConfigs():
    SshConfig.ssh_user = privateConfigs.ssh_user  # your server root privileges user ex : "root"
    SshConfig.ssh_ip = privateConfigs.ssh_ip  # your server ip adress ex : "192.168.2.1"
    SshConfig.ssh_password = privateConfigs.ssh_password  # your server password ex:"myPassword123"


def bindSiteConfigs():
    SiteConfig.site_folder_name = privateConfigs.site_folder_name  # only site folder name ex: my_project
    SiteConfig.domain_list = privateConfigs.domain_list  # nginx domain list its must be string and 1 space each domain ex:"mydomain.com www.mydomain.com"
    # SiteConfig.github_repo_url = privateConfigs.github_repo_url  # your web site github repo url  ex : "https://github.com/your_username/your_repo_url.git"
    SiteConfig.github_user_name = privateConfigs.github_user_name
    SiteConfig.github_password = privateConfigs.github_password
    SiteConfig.github_repository_name = privateConfigs.github_repository_name
    # SiteConfig.static_file_folder = privateConfigs.stat
    print("site config writed")


def bindGeneralConfigs():
    """
    parent folder with all sites ex :"/var/www/vhost/" ex2:"/home/murat/"
    it's must be start with / and must be end with /
    :return:
    """
    GeneralConfigs.sites_container_folder = privateConfigs.sites_container_folder


"""
 bu dosya baştan yazıldığı için  change edilmiyor
"""


def createLaravelDeployScriptFields():
    with open('scripts/laravelDeployScript', 'r') as file:
        data = file.readlines()
        data.clear()
    # now change the 2nd line, note that you have to add a newline
    data.insert(0, 'cd %s \n' % GeneralConfigs.sites_container_folder)
    data.insert(1, 'mkdir %s \n' % SiteConfig.site_folder_name)
    data.insert(2, 'cd %s \n' % SiteConfig.site_folder_name)
    data.insert(3, 'git clone https://%s:%s@github.com/%s/%s.git .\n' % (SiteConfig.github_user_name, SiteConfig.github_password, SiteConfig.github_user_name, SiteConfig.github_repository_name))
    data.insert(4, 'composer install\n')
    data.insert(5, 'php artisan key:generate\n')
    data.insert(5, 'composer dump-autoload\n')

    with open('scripts/laravelDeployScript', 'w') as file:
        file.writelines(data)
    print("======script file processing===")
    print(data)


def pushLaravelDeployScriptToServer():
    print("script pushing to server")
    # system("sudo apt-get install sshpass")
    system("ssh %s@%s 'bash -s' < 'scripts/laravelDeployScript'" % (SshConfig.ssh_user, SshConfig.ssh_ip))


def prepareServerBeforeDeploying():
    print("==========server some packages installed such as NGINX - PHP")
    # system("ssh %s@%s 'bash -s' < 'scripts/serverPrepareScript'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("sshpass -p '%s' ssh  %s@%s 'bash -s' < 'scripts/serverPrepareScript'" % (SshConfig.ssh_password,SshConfig.ssh_user, SshConfig.ssh_ip))


def index():
    print("""
    ===================================================================
    =                                                                 =
    = Welcome to Laravel Auto Deployer created by github.com@muratenes 
    = > You should be firstly upload web site to  github
    = > Create requirements.txt and write to project requirements in project folder
    = > You must install server requirements
    =   -sudo apt-get update
    =   -sudo apt-get install nginx python3-pip python3-dev                                   =
    ===================================================================
    """)
    # deleteServerOldConfAndDataFromServer(SiteConfig, SshConfig, GeneralConfigs)
    # laraConf.setToDefaultScripts()
    # bindSshConfigs()
    # bindSiteConfigs()
    # bindGeneralConfigs()
    createLaravelDeployScriptFields()
    # prepareServerBeforeDeploying()
    pushLaravelDeployScriptToServer()
    laraConf.createNginxFile(SiteConfig, SshConfig, GeneralConfigs)
    laraConf.pushToNginxFileToServer(SiteConfig, SshConfig, GeneralConfigs)
    system("ssh %s@%s 'systemctl restart nginx.service'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    # system("ssh %s@%s 'systemctl daemon-reload'")
    system("ssh %s@%s 'cat /var/log/nginx/error.log'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("ssh %s@%s 'sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled'" % (SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))
    system("ssh %s@%s 'sudo chmod 755 -R %s%s/storage'" % (SshConfig.ssh_user, SshConfig.ssh_ip, GeneralConfigs.sites_container_folder,SiteConfig.site_folder_name))
    system("ssh %s@%s 'sudo chmod -R o+w %s%s/storage'" % (SshConfig.ssh_user, SshConfig.ssh_ip, GeneralConfigs.sites_container_folder,SiteConfig.site_folder_name))
    system("ssh %s@%s 'sudo chmod -R o+w %s%s/public/uploads'" % (SshConfig.ssh_user, SshConfig.ssh_ip, GeneralConfigs.sites_container_folder,SiteConfig.site_folder_name))


def deleteServerOldConfAndDataFromServer(siteConfig, sshConfig, generalConfig):
    print("====== WARNING : DELETED OLD CONF FILES =======")
    laraConf.replaceText("scripts/deleteOldDatasScript", "parent_folder", generalConfig.sites_container_folder)
    laraConf.replaceText("scripts/deleteOldDatasScript", "site_folder", siteConfig.site_folder_name)
    with open('scripts/deleteOldDatasScript', 'r') as file:
        data = file.readlines()
        data.clear()
    system("ssh %s@%s 'bash -s' < 'scripts/deleteOldDatasScript'" % (sshConfig.ssh_user, sshConfig.ssh_ip))
    laraConf.setToDefaultScripts()


if __name__ == '__main__':
    laraConf.setToDefaultScripts()
    bindSshConfigs()
    bindSiteConfigs()
    bindGeneralConfigs()
    if int(sys.argv.__len__()) > 1:
        print(sys.argv)
        for i, arg in enumerate(sys.argv):
            if i > 0:
                if str(arg) == "delete-old":
                    print("delet old var")
                    deleteServerOldConfAndDataFromServer(SiteConfig, SshConfig, GeneralConfigs)
            # args = [(sys.argv[1]), (sys.argv[2])]
    else:
        index()

        # index()

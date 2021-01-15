class SshConfig():
    ssh_user = None
    ssh_password = None
    ssh_ip = None
    ssh_port = None

    def print(self):
        print("""
        ======= SSH Configs =========
        ssh User  = %s
        ssh_password = %s
        ssh_ip =  %s
        ssh_port =  %s
        """)


# burası index.py'dan dolduruluyor null kalmalıdır
class SiteConfig():
    site_folder_name = None
    domain_list = None  # arasında 1 boşluk bırakarak yazınız
    github_repo_url = None
    github_user_name = None
    github_password = None
    github_repository_name = None
    static_file_folder = None


class GeneralConfigs():
    sites_container_folder = None

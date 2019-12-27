import os
import requests
from tempfile import NamedTemporaryFile

from smb.SMBConnection import SMBConnection


class SambaSynchro:
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.smb_path = config["smb_path"]
        self.device_path = os.path.join(os.getcwd(), config["device_path"])
        self.device_temp_data = os.path.join(os.getcwd(), config["device_path"])
        self.client = config["client"]
        self.ip = config["router_ip"]
        self.username = config["username"]
        self.is_conn = False
        self.password = config["password"]
        self.share_name = config["share_name"]

    def connect(self):
        self.server = SMBConnection(
            self.username,
            self.password,
            self.client,
            "",
            use_ntlm_v2=True,
            is_direct_tcp=True,
        )
        isok = self.server.connect(self.ip, 139)
        if isok:
            print("isok")
        else:
            print("not ok")

    def is_connected(self):
        try:
            requests.get("http://" + self.ip, timeout=1)
            return True
        except requests.ConnectionError as err:
            return False

    def listFiles(self):
        self.connect()
        files = self.server.listPath(self.share_name, self.smb_path)
        filenames = [f.filename for f in files]
        self.server.close()
        filenames = [f for f in filenames if (len(f) == 10 and f[2] == "_")]
        filenames.sort()
        return filenames

    def target_path(self, fname):
        return os.path.join(self.device_path, fname)

    def download(self, k=0, names=None):
        # k=0 -> download all, k>0 -> download k files.
        if self.is_connected():
            files = self.listFiles()
            if k > 0:
                files = files[-k:]
            if isinstance(names, type(None)):
                names = files
            nrows = []
            self.connect()
            dwn = []
            for smb_file_name in files:
                if smb_file_name in names:
                    with NamedTemporaryFile() as tmp:
                        fname = os.path.join(self.smb_path, smb_file_name)
                        _, filesize = self.server.retrieveFile(
                            self.share_name, fname, tmp
                        )
                        tmp.file.seek(0)
                        smb_file_content = tmp.file.read().decode()
                        with open(self.target_path(smb_file_name), "w") as f:
                            f.write(smb_file_content)
                            n = sum([1 for i in smb_file_content if i == "{"])
                            nrows.append(n)
                        dwn.append(smb_file_name)
            self.server.close()
            self.txt_dwn = (
                "Data \n%s\n successfully downloaded (items number: \n%s)"
                % (dwn, nrows)
            )
        else:
            self.txt_dwn = "Connection error :("

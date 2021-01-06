import requests
import time
import shutil
import tarfile
import gzip
import os
import tempfile
import copy
from pathlib import Path

loginUri = "https://AscomServer/phpgui/login.php"
backupUri = "https://AscomServer/cgi-bin/admin/getbackup"
payload = {"username": "", "password": ""}
# headers = {"Content-Type":"multipart/form-data"}
filename = "{}_unite_communication_server-1.5.0-backup".format(time.strftime("%Y%m%d%H%M%S"))
downloadDir = "download/src/"
gzip_suffix = ".gzip"
tar_suffix = ".tar"
gzipRaw = None

def main():
    local_filename = Path(downloadDir, filename).with_suffix(gzip_suffix)
    # print("DownloadFile: {}".format(local_filename))
    # print(loginUri)
    with tempfile.TemporaryDirectory() as tmpdir:
        with requests.Session() as session:
            post = session.post(loginUri, data=payload, verify=False)
            with session.get(backupUri, verify=False, stream=True) as r:
                with open(Path(tmpdir,filename).with_suffix(gzip_suffix), "wb") as f:
                    shutil.copyfileobj(r.raw, f)

                with gzip.open(Path(tmpdir,filename).with_suffix(gzip_suffix), 'rb') as gz:
                    content = gz.read()

                    with open(Path(tmpdir,filename).with_suffix(tar_suffix), 'wb') as f:
                        f.write(content)

                    tar = tarfile.open(Path(tmpdir,filename).with_suffix(tar_suffix), mode='r')
                    tar.extractall(path=Path(downloadDir,filename))
          
        requests.session().close()
# Mount sqlite

# query sqlite

# process query results


if __name__ == "__main__":
    main()

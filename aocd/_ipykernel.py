from __future__ import annotations

import os
import re

import urllib3


def get_ipynb_path():
    # helper function so that "from aocd import data" can introspect the year/day from
    # the .ipynb filename. inline imports to avoid hard-dependency on IPython/jupyter
    from jupyter_server import serverapp
    from jupyter_server.utils import url_path_join

    from IPython.core.getipython import get_ipython


    ipython = get_ipython()
    assert ipython is not None

    app = ipython.config["IPKernelApp"]
    search = re.search(r"(?<=kernel-)[\w\-]+(?=\.json)", app["connection_file"])
    assert search is not None
    kernel_id = search[0]
    http = urllib3.PoolManager()
    for serv in serverapp.list_running_servers():
        url = url_path_join(serv["url"], "api/sessions")
        resp = http.request("GET", url, fields={"token": serv["token"]})
        if resp.status >= 400:
            raise urllib3.exceptions.ResponseError(f"HTTP {resp.status}")
        for sess in resp.json():
            if kernel_id == sess["kernel"]["id"]:
                path = serv["root_dir"]
                fname = sess["notebook"]["path"]
                return os.path.join(path, fname)

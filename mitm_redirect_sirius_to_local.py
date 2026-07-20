"""Redirect the official game API + assets to the local emulator.

mitmproxy -s mitm_redirect_sirius_to_local.py
mitmproxy -s mitm_redirect_sirius_to_local.py -s mitmweb_helper.py
"""

from __future__ import annotations

from mitmproxy import http
import socket

do_proxying = False
local_assets = True  # redirect asset requests to the local server (if downloaded)

LOCAL_PORT = 8123
API_HOST = "lb-api.wds-stellarium.com"
ASSET_HOST = "assets-e.wds-stellarium.com"
REALTIME_HOST = "lb-realtime.wds-stellarium.com"


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("1.1.1.1", 80))
IP_ADDR = s.getsockname()[0]
print("Redirecting to {}:{}".format(IP_ADDR, LOCAL_PORT))

def request(flow: http.HTTPFlow) -> None:
    if not do_proxying:
        return
    
    host = flow.request.pretty_host

    # redirect the official API to the local emulator
    if host == API_HOST:
        flow.request.host = IP_ADDR
        flow.request.port = LOCAL_PORT
        flow.request.scheme = "http"
        flow.request.headers["Host"] = host
        
    # redirect the official realtime server to the local emulator
    elif host == REALTIME_HOST:
        flow.request.host = IP_ADDR
        flow.request.port = LOCAL_PORT
        flow.request.scheme = "http"
        flow.request.headers["Host"] = host

    # redirect the official asset server to the local emulator
    elif host == ASSET_HOST:
        if not local_assets:
            return
        
        flow.request.host = IP_ADDR
        flow.request.port = LOCAL_PORT
        flow.request.scheme = "http"
        flow.request.headers["Host"] = host
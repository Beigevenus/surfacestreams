#!/usr/bin/python3

import sys,gi,json
gi.require_version('GLib', '2.0')
gi.require_version('Gst',  '1.0')
gi.require_version('Soup', '2.4')
gi.require_version('GstWebRTC', '1.0')
gi.require_version('GstSdp', '1.0')
from gi.repository import GLib, Gst, Soup, GstWebRTC, GstSdp

from gst_helpers import *
from webrtc_peer import WebRTCPeer

pipeline = None
clients = {}

# incoming HTTP(S) request
def http_handler(server,msg,path,query,client,user_data):
    content_type = "text/html"
    try:
        data = open(path[1:],"r").read()
        if path.endswith(".js"):
            content_type = "text/javascript"
    except:
        msg.set_status(Soup.Status.NOT_FOUND)
        return
    msg.response_headers.append("Content-Type",content_type)
    msg.response_body.append(data.encode("utf-8"))
    msg.set_status(Soup.Status.OK)

# Websocket connection was closed by remote
def ws_close_handler(connection, wrb):
    # TODO actually handle closing (might be tricky, needs to rewire pipeline)
    print("WebSocket closed by remote.")

# incoming Websocket connection
def ws_conn_handler(server, connection, path, client, user_data):

    addr = client.get_remote_address()
    source = addr.get_address().to_string()+"_"+str(addr.get_port())
    print("New WebSocket connection from "+source)

    wrb = WebRTCPeer(connection,source)
    connection.connect("closed",ws_close_handler,wrb)
    clients[source] = wrb

# "main"
init_pipeline()

add_and_link([
    new_element("videotestsrc",{"is-live":True,"pattern":"ball"}),
    new_element("capsfilter",{"caps":Gst.Caps.from_string("video/x-raw,format=YV12,width=640,height=360,framerate=15/1")}),
    new_element("tee",{"allow-not-linked":True},"testsource")
])

add_and_link([
    new_element("audiotestsrc",{"is-live":True,"wave":"ticks"}),
    new_element("capsfilter",{"caps":Gst.Caps.from_string("audio/x-raw,format=U8,rate=8000,channels=1")}),
    new_element("tee",{"allow-not-linked":True},"audiotest")
])

server = Soup.Server()
server.add_handler("/",http_handler,None)
server.add_websocket_handler("/ws",None,None,ws_conn_handler,None)
server.set_ssl_cert_file("cert.pem","key.pem")
server.listen_all(8080,Soup.ServerListenOptions.HTTPS)

run_mainloop()

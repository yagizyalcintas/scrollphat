
import requests
import socket
import time
import json
import _thread
from random import randint
from flask import Flask, request, abort
from td import get_td
import scrollphathd


# ---------------- CONFIG ----------------
TD_DIRECTORY_ADDRESS = "http://192.168.0.100:8080"
LISTENING_PORT = 8080
DEFAULT_BRIGHTNESS = 0.5


app = Flask(__name__)



@app.route("/")
def thing_description():
    return json.dumps(get_td(ip_addr)), {'Content-Type': 'application/json'}


@app.route("/properties/display_size", methods=["GET"])
def display_size():
    return scrollphathd.get_shape() , {'Content-Type': 'application/json'}


@app.route("/properties/buffer_size", methods=["GET"])
def display_size():
    return scrollphathd.get_buffer_shape(), {'Content-Type': 'application/json'}


@app.route("/actions/set_pixel", methods=["POST"])
def setPixel():
    if request.is_json:
        try:
            bright = float(request.json["brightness"])
            x = int(request.json["x"])
            y = int(request.json["y"])
            scrollphathd.clear()
            scrollphathd.show()
            scrollphathd.set_pixel(x, y, bright)
            scrollphathd.show()
            return "", 204
        except Exception as e:
            print(e)
            abort(400)
    else:
        abort(415)  # Wrong media type.

@app.route("/actions/write_string", methods=["POST"])
def writeString():
    if request.is_json:
        try:
            Str = str(request.json["string"])
            x = int(request.json["x"])
            y = int(request.json["y"])
            bright = float(request.json["brightness"])
            mono = request.json["monospaced"]
            scrollphathd.clear()
            scrollphathd.show()
            scrollphathd.write_string(Str, x, y, font=None, letter_spacing=1, brightness = bright , monospaced = mono, fill_background=False)
            scrollphathd.show()
            return "", 204
        except Exception as e:
            print(e)
            abort(400)
    else:
        abort(415)  # Wrong media type.

@app.route("/actions/write_char", methods=["POST"])
def writeChar():
    if request.is_json:
        Char = chr(request.json["string"])
        o_x = int(request.json["x"])
        o_y = int(request.json["y"])
        bright = float(request.json["brightness"])
        mono = request.json["monospaced"]
        scrollphathd.clear()
        scrollphathd.show()
        scrollphathd.draw_char(o_x, o_y, Char, font=None, brightness=bright, monospaced=mono)
        scrollphathd.show()
        return "", 204
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/display_graph", methods=["POST"])
def displayGraph():
    if request.is_json:
        x = int(request.json["x"])
        y = int(request.json["y"])
        bright = float(request.json["brightness"])
        val = request.json["values"]
        w = request.json["width"]
        h = request.json["height"]
        scrollphathd.clear()
        scrollphathd.show()
        scrollphathd.set_graph(val, low=None, high=None, brightness=bright, x = x, y = y, width = w, height=h)
        scrollphathd.show()
        return "", 204
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/fill", methods=["POST"])
def fillArea():
    if request.is_json:
        x = int(request.json["x"])
        y = int(request.json["y"])
        bright = float(request.json["brightness"])
        w = request.json["width"]
        h = request.json["height"]
        scrollphathd.clear()
        scrollphathd.show()
        scrollphathd.fill(brightness, x=x, y=y, width=w, height=h)
        scrollphathd.show()
        return "", 204
    else:
        abort(415)  # Wrong media type.

@app.route("/actions/clear_rect", methods=["POST"])
def clearArea():
    if request.is_json:
        x = int(request.json["x"])
        y = int(request.json["y"])
        w = request.json["width"]
        h = request.json["height"]
        scrollphathd.clear_rect(x, y, w, h)
        scrollphathd.show()
        return "", 204
    else:
        abort(415)  # Wrong media type.

@app.route("/actions/clear", methods=["POST"])
def Clear():
    if request.is_json:
        x = int(request.json["x"])
        y = int(request.json["y"])
        w = request.json["width"]
        h = request.json["height"]
        scrollphathd.clear()
        scrollphathd.show()

        return "", 204
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/shutdown", methods=["POST"])
def shutdown():
    for i in range(NR_OF_LEDS):
        dots[i] = (0, 0, 0)
    return "", 204


def submit_td(ip_addr):
    td = get_td(ip_addr)
    print("Uploading TD to directory ...")
    while True:
        try:
            r = requests.post("{}/td".format(TD_DIRECTORY_ADDRESS), json=td)
            r.close()
            print("Got response: ", r.status_code)
            if 200 <= r.status_code <= 299:
                print("TD uploaded!")
                return
        except Exception as e:
            print(e)
            print("TD could not be uploaded. Will try again in 15 Seconds...")
            time.sleep(15)


# wait for Wifi to connect
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        s.connect(('192.168.0.1', 80))  # connect to router to ensure a successful connection
        ip_addr = s.getsockname()[0] + ":" + str(LISTENING_PORT)
        break
    except OSError:
        time.sleep(3)

# Submit TD to directory
_thread.start_new_thread(submit_td, (ip_addr))

# Run app server
app.run(host='0.0.0.0', port=8080)

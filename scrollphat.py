import requests
import socket
import time
import json
import _thread
from random import randint
from flask import Flask, request, abort
from phatTD import get_td
import scrollphathd
from jsonschema import Draft6Validator

# ---------------- CONFIG ----------------
TD_DIRECTORY_ADDRESS = "http://172.16.1.100:8080"
LISTENING_PORT = 8080
DEFAULT_BRIGHTNESS = 0.5

td = 0
app = Flask(__name__)


@app.route("/")
def thing_description():
    return json.dumps(get_td(ip_addr)), {'Content-Type': 'application/json'}


@app.route("/properties/display_size", methods=["GET"])
def display_size():
    return str(scrollphathd.get_shape()), {'Content-Type': 'application/json'}


@app.route("/actions/set_pixel", methods=["POST"])
def setPixel():
    if request.is_json:
        schema = td["actions"]["set_pixel"]["input"]
        valid_input = Draft6Validator(schema).is_valid(request.json)

        if valid_input:
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
            abort(400)
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/write_string", methods=["POST"])
def writeString():
    if request.is_json:
        schema = td["actions"]["write_string"]["input"]
        valid_input = Draft6Validator(schema).is_valid(request.json)

        if valid_input:
            dur = 5
            count = 0
            try:
                try:
                    dur = int(request.json["time"])
                except Exception as e:
                    print(e)
                Str = " " + str(request.json["string"])
                print(Str)
                x = int(request.json["x"])
                print(x)
                y = int(request.json["y"])
                print(y)
                bright = float(request.json["brightness"])
            
                scrollphathd.clear()
                scrollphathd.show()
                scrollphathd.write_string(Str, x, y, font=None, letter_spacing=1, brightness=bright, monospaced=True, fill_background=False)
                scrollphathd.flip(x=True, y=True)

                while count < dur*10:
                    scrollphathd.show()
                    scrollphathd.scroll(1)
                    time.sleep(0.05)
                    count = count + 1
                scrollphathd.clear()
                scrollphathd.show()
                return "", 204
            except Exception as e:
                print(e)
                abort(400)
        else:
            abort(400)
            print("wrong input")
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/write_char", methods=["POST"])
def writeChar():
    if request.is_json:
        schema = td["actions"]["write_char"]["input"]
        valid_input = Draft6Validator(schema).is_valid(request.json)

        if valid_input:
            Char = str(request.json["char"])
            o_x = int(request.json["o_x"])
            o_y = int(request.json["o_y"])
            bright = float(request.json["brightness"])

            scrollphathd.clear()
            scrollphathd.show()
            scrollphathd.draw_char(o_x, o_y, Char, font=None,brightness=bright, monospaced=True)
            scrollphathd.flip(x=True, y=True)
            scrollphathd.show()
            time.sleep(3)
            return "", 204
        else:
            abort(400)
            print("wrong input")
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/fill", methods=["POST"])
def fillArea():
    if request.is_json:
        schema = td["actions"]["fill"]["input"]
        valid_input = Draft6Validator(schema).is_valid(request.json)

        if valid_input:
            x = 0
            y = 0
            w = 17
            h = 6
            try:
                x = int(request.json["x"])
            except Exception as e:
                print(e)
            try:
                y = int(request.json["y"])
            except Exception as e:
                print(e)
            try:
                w = request.json["width"]
            except Exception as e:
                print(e)
            bright = float(request.json["brightness"])
            try:
                h = request.json["height"]
            except Exception as e:
                print(e)
            scrollphathd.clear()
            scrollphathd.show()
            scrollphathd.fill(brightness=bright, x=x, y=y, width=w, height=h)
            scrollphathd.show()
            return "", 204
        else:
            abort(400)
            print("wrong input")
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/clear_rect", methods=["POST"])
def clearArea():
    if request.is_json:
        schema = td["actions"]["clear_rect"]["input"]
        valid_input = Draft6Validator(schema).is_valid(request.json)

        if valid_input:
            x = 0
            y = 0
            w = 17
            h = 6
            try:
                x = int(request.json["x"])
            except Exception as e:
                print(e)
            try:
                y = int(request.json["y"])
            except Exception as e:
                print(e)
            try:
                w = request.json["width"]
            except Exception as e:
                print(e)
            try:
                h = request.json["height"]
            except Exception as e:
                print(e)
            scrollphathd.clear_rect(x, y, w, h)
            scrollphathd.show()
            return "", 204
        else:
            abort(400)
            print("wrong input")
    else:
        abort(415)  # Wrong media type.


@app.route("/actions/clear", methods=["POST"])
def Clear():
    if request.is_json:

        scrollphathd.clear()
        scrollphathd.show()

        return "", 204
    else:
        abort(415)  # Wrong media type.


def submit_td(ip_addr, tdd_address):
    global td 
    td = get_td(ip_addr)
    print("Uploading TD to directory ...")
    while True:
        try:
            r = requests.post("{}/td".format(tdd_address), json=td)
            r.close()
            print("Got response: ", r.status_code)
            if 200 <= r.status_code <= 299:
                print("TD uploaded!")
                return
            else:
                print("TD could not be uploaded. Will try again in 15 Seconds...")
                time.sleep(15)
        except Exception as e:
            print(e)
            print("TD could not be uploaded. Will try again in 15 Seconds...")
            time.sleep(15)


# wait for Wifi to connect
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        # connect to router to ensure a successful connection
        s.connect(('172.16.1.1', 80))
        ip_addr = s.getsockname()[0] + ":" + str(LISTENING_PORT)
        break
    except OSError:
        time.sleep(5)

# Submit TD to directory
_thread.start_new_thread(submit_td, (ip_addr, TD_DIRECTORY_ADDRESS))

# Run app server
app.run(host='0.0.0.0', port=8080)

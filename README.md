## bt2: Blaze Telegram Backdoor Toolkit

bt2 is a Python-based backdoor in form of a IM bot that uses the
infrastructure and the feature-rich bot API provided by Telegram, slightly
repurposing its communication platform to act as a C&C.

## Dependencies

* [Telepot](https://github.com/nickoala/telepot)
* [requests](https://pypi.python.org/pypi/requests/)

## Installation

```
$ sudo pip install telepot
$ sudo pip install requests
```

PS: Telepot requires minimum of requests 2.9.1 to work properly.

## Limitations

Currently the shellcode execution component is dependent on ctypes and
works only on Windows platforms.

## Usage

Before using this code one has to register a bot with Telegram. This can
be done by talking to Botfather - after setting up the name for the bot and
username you will get a key that will be used to interact with the bot API.

For more information see [Telegram bots: an introduction for developers](https://core.telegram.org/bots#botfather)

Also, it is highly advisable to replace 'botmaster ID' with the ID of the
master, locking the communication between the bot to the specific ID of
the botmaster to avoid abuse from unauthorized parties.

```
$ python bt2.py
```

![Sample screenshot](https://raw.githubusercontent.com/blazeinfosec/bt2/master/images/screenshot.png)

## Resources

We will soon launch a blog post with all details about the tool, so watch
this space.

## Disclaimer

bt2 is a mere proof of concept and by no means intends to breach the terms
and conditions of Telegram. It was developed for usage in legitimate
penetration testing engagements and neither the author nor Blaze
Information Security can be liable for any malicious use of the tool.

## Known bugs

* After launching a reverse shell and exiting from it, all commands sent to
the bot have duplicate responses.

## Author

* **Julio Cesar Fort** - julio at blazeinfosec dot com
* Twitter: @juliocesarfort / @blazeinfosec

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

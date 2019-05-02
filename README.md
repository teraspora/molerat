# Molerat Messenger: A simple UDP subnet messenger program

## Requires Python 3: run in terminal: `python3 molerat.py`

Run it on another computer too, and send text messages back and forth.

Note: the program uses UDP, which does not guarantee delivery; some messages may therefore not arrive, and so the program should not be used for critical systems.

So far only tested on two Linux boxes.   Needs testing on Windows and OSX.

## Update

I've just been informed that the ANSI colour codes don't work in Windows, and neither does the line

`this_ip = os.popen('hostname -I').read()[:-2]`, resulting in the error

`Use Network Control Panel Applet to set hostname
hostname -s is not supported.`

So I need to find out a way to get colour output in the Windos command shell, and to implement different colour codes dependent on operating system.


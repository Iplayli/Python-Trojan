# Python-Trojan
A Python Trojan, giving you (almost) full terminal access over your victims pc. [This is for educational purposes ONLY]

In the slave.py script enter the ip adress of your own pc. Then (auto)run the script on the victim pc. Whenever you feel like it, you can then start connecting by running your local script. Now you have (almost) full terminal controll, including self-script functions like upload and download.

The code is written in Python and if you want to run this on someones pc, the pc needs to have Python installed. However, you can transform those 2 files into .exe by using e.g. Pyinstaller (you will find tutorials to this on the internet). The only reason I didnt upload .exe was because editing the .py files is way easier and you will still have to change the ip adress, so the .exe's would be worthless.

For those who don't know, in order to autorun a script on startup press "win + R" enter "shell:startup" and put the file in that folder. Whenever the victims pc boots now, the programm will automatically start running. 

You should change the slave.py to slave.pyw, this makes it so that the console window doesnt open and your victim doesnt see that he's getting hacked. If you are using pyinstaller, add --windowed when creating your exe. This has exactly the same effect.


Possible Improvements:

To make it more secure you could change it so that the victim pc doesnt have your ip adress in their script, but you theirs. Only problem is that if the victim pc changes its ip adress, you wont be able to connect anymore, unless you find out the new ip adress. In the current version you are always able to connect if you just know what ip adress you need to have in order to connect to the other script.

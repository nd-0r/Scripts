import signal
import os
import random
import time

voices = [
        "Agnes     ", 
        "Albert    ", 
        "Alex      ", 
        "Alice     ", 
        "Allison   ", 
        "Alva      ", 
        "Amelie    ", 
        "Anna      ", 
        "Ava       ", 
        "Bad News  ", 
        "Bahh      ", 
        "Bells     ", 
        "Boing     ", 
        "Bruce     ", 
        "Bubbles   ", 
        "Carmit    ", 
        "Cellos    ", 
        "Damayanti ", 
        "Daniel    ", 
        "Deranged  ", 
        "Diego     ", 
        "Ellen     ", 
        "Fiona     ", 
        "Fred      ", 
        "Good News ", 
        "Hysterical", 
        "Ioana     ", 
        "Joana     ", 
        "Jorge     ", 
        "Juan      ", 
        "Junior    ", 
        "Kanya     ", 
        "Karen     ", 
        "Kathy     ", 
        "Kyoko     ", 
        "Laura     ", 
        "Lekha     ", 
        "Luca      ", 
        "Luciana   ", 
        "Maged     ", 
        "Mariska   ", 
        "Mei-Jia   ", 
        "Melina    ", 
        "Milena    ", 
        "Moira     ", 
        "Monica    ", 
        "Nora      ", 
        "Paulina   ", 
        "Pipe Organ", 
        "Princess  ", 
        "Ralph     ", 
        "Rishi     ", 
        "Samantha  ", 
        "Sara      ", 
        "Satu      ", 
        "Sin-ji    ", 
        "Susan     ", 
        "Tessa     ", 
        "Thomas    ", 
        "Ting-Ting ", 
        "Tom       ", 
        "Trinoids  ", 
        "Veena     ", 
        "Vicki     ", 
        "Victoria  ", 
        "Whisper   ", 
        "Xander    ", 
        "Yelda     ", 
        "Yuna      ", 
        "Yuri      ", 
        "Zarvox    ", 
        "Zosia     ", 
        "Zuzana    "
        ]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

interrupted = False
while True:
       os.system("say -r 350 -v " + voices[random.randint(0, len(voices) - 1)] + " Hey! Wake up!")
       time.sleep(random.randint(120, 600))

       if interrupted:
           print("Done!")
           break


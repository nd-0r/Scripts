import time
import math
import os

commands = {
  "message_all": "/msg @a ",
  "weather_clear": "/weather clear",
  "weather_thunder": "/weather thunder",
  "time_night": "/time set night",
  "time_day": "/time set day"
}
clear_day_strings = ['sunny weather', 'sunny', 'wonderful day', 'beautiful day', 'bright day', 'fine day', 'lovely day']
night_strings = ['night', 'evening', 'dark', 'tonight', 'nighttime', 'overnight', 'darkness', 'nightfall', 'twilight', 'midnight']
storm_strings = ['storm', 'rainstorm', 'tempest', 'hurricane', 'thunder', 'thunderstorm', 'stormy']

shell_command = "/opt/minecraft/tools/mcrcon/mcrcon -p $(cat /opt/minecraft/tools/passwd.txt) "

def read_script():
  lines = []
  with open('./trumanshow.txt') as ts:
    lines = ts.readlines()

  primary_command = ''
  for line in lines[:20]:
    primary_command = shell_command + '"' + commands["message_all"] + line.strip() + '"'
    for day_phrase, night_phrase in zip(clear_day_strings, night_strings):
      if (day_phrase in line):
        primary_command += " && " + shell_command + '"' + commands["weather_clear"] + '"'
        primary_command += " && " + shell_command + '"' + commands["time_day"] + '"'
      elif (night_phrase in line):
        primary_command += " && " + shell_command + '"' + commands["time_night"] + '"'
    for storm_phrase in storm_strings:
      if (storm_phrase in line and ('clear' not in primary_command)):
        primary_command += " && " + shell_command + '"' + commands["weather_thunder"] + '"'
    os.system(primary_command)
    time.sleep(math.sqrt(len(line) / 10))

if __name__ == '__main__':
  read_script()
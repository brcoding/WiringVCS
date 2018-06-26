from os import listdir
from os.path import isfile, join
import hashlib
import time
import RPi.GPIO as gpio
import subprocess

# Set this to the CS select pin.
testpin = 8
read_size = 32
rom_path = "roms"
# Get the list of roms in the roms folder
files = [f for f in listdir(rom_path) if isfile(join(rom_path, f))]

def run_cart():
  stella = None
  try:
    print("Cart inserted, dumping rom.")
    # Dump the connected cart to rom.bin
    subprocess.call(["./dumper"])
    # Reset the pin so we can detect when it is pulled out.
    gpio.setmode(gpio.BCM)
    gpio.setup(testpin, gpio.OUT, initial=gpio.LOW)
    gpio.setup(testpin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.remove_event_detect(testpin)
    gpio.add_event_detect(testpin, gpio.BOTH)
    def pin_callback(data):
      print("Cart Removed")
      try:
        stella.terminate()
      except OSError:
        pass
    gpio.add_event_callback(testpin, pin_callback)
    
    digest = ""
    with open("rom.bin") as f:
      digest = hashlib.sha224(f.read(read_size)).hexdigest()
    #digest = hashlib.sha224(data).hexdigest()
    print("Cart Hash: {}".format(digest))
    for file in files:
      with open(rom_path + "/" + file, 'rb') as f:    
        if digest == hashlib.sha224(f.read(read_size)).hexdigest():
          print("Found hash: {} Filename: {}".format(digest, file))
          #call(["stella", rom_path + "/" + file])
          stella = subprocess.Popen(["stella", rom_path + "/" + file], shell=False)
          stella.wait()
          gpio.cleanup()
          break
  except Exception as e:
    print("Exception while trying to read cart: {}".format(e))

try:
  while True:
    # Setup GPIO to detect when the CS Select pin is high (the cart is connected)
    gpio.setmode(gpio.BCM)
    gpio.setup(testpin, gpio.OUT, initial=gpio.LOW)
    gpio.setup(testpin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    print("Waiting for a cart...")
    while True:
      time.sleep(1)
      if gpio.input(testpin) == 0:
        break
    # Give a second to make sure the cart is all the way plugged in before trying to read.
    time.sleep(1)
    gpio.cleanup()

    run_cart()
except KeyboardInterrupt:
  pass

print("Exiting...")
gpio.cleanup()

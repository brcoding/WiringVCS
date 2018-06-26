# Python Launcher

This is a simple script that reads the first 32 bytes of a ROM and then looks in a folder of already dumped roms. If it finds a match it will launch that previously dumped rom.  This lets you plug your Cart in and just use it as a starting point. Most Carts are quite dirty and can have poor connections. This just increases the chances of a clean run with a potentially dirty connection.

The script will detect when the cart has been plugged in by reading the CS pin and then launch dumper.

## Setup

Install Python (any version)

```
sudo apt-get install python
```

Setup Virtual Env:

```
sudo pip install virtualenv
```

Setup the libraries used:

```
sudo pip install -r /path/to/requirements.txt
```

## Running

```
python launcher.py
```

After it has started simply plug in your cart and play.  You may need to change the roms folder at the top of the script. Also, if you have used a different pin you may need to adjust the BCM pin for the CS select pin.

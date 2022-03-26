#!/usr/bin/env python3
import sys
import subprocess
import shutil

LATENCY = 1

# Make sure Ultrastar is in our PATH
if shutil.which("ultrastardx") is None:
  print("Error: ultrastardx executable not found, make sure it's in your PATH")
  sys.exit(1)

# Get list of USB-connected sources from PulseAudio
devices = list()
ret = subprocess.run(['pactl', 'list', 'short'], capture_output=True)
for line in ret.stdout.decode("utf-8").splitlines():
  tokens = line.split()
  if (len(tokens) > 1 and tokens[1].startswith("alsa_input.usb")):
    devices.append(tokens[1])

# Create mic loopbacks, save returned index for unloading afterwards
indices = list()
for device in devices:
  command = ['pactl', 'load-module', 'module-loopback', f'source={device}', f'latency_msec={str(LATENCY)}']
  ret = subprocess.run(command, capture_output=True)  
  if (ret.returncode == 0):
    indices.append(ret.stdout.decode("utf-8").splitlines()[0])

# Launch Ultrastar Deluxe
command = ['ultrastardx']
if len(sys.argv) > 1:
  command += sys.argv[1:]
subprocess.run(command)
  
# Unload mic loopbacks
for index in indices:
  command = ['pactl', 'unload-module', index]
  subprocess.run(command)

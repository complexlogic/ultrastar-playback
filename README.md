# ultrastar-playback
The Ultrastar Deluxe karaoke game has a microphone playback feature which outputs the recorded microphone audio to the speakers so singers can hear themselves, which provides a more authentic karaoke experience. Unfortunately, the feature is entirely unusable in its current state due to excessive latency and audio crackling. The devs have [acknowledged](https://github.com/UltraStar-Deluxe/USDX/issues/518) this and stated that there are no plans to fix it. Instead, they suggest that the microphone playback should be implemented at the OS level. However, the suggested workaround is Windows-specific. This repo contains a Python script which implements the feature on Linux using the PulseAudio [module-loopback](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#module-loopback) module.

The script detects all USB-connected audio sources, sets up a loopback in PulseAudio for each of them, launches Ultrastar Deluxe, then unloads each loopback after the game is finished.

## Usage
You may use this script to implement the microphone playback feature on Linux if all of the following conditions apply:
- You use PulseAudio as your audio backend
- You use USB microphones (it will not work with analog ones)
- The ```ultrastardx``` executable is in your PATH

To use, download the script and set it to executable with ```chmod```.  The script has a shebang which will automatically invoke the Python interpreter. Use the path of the script to run it:
```
/path/to/ultrastar-playback.py
```
Any arguments given to the script will be passed through to the ```ultrastardx``` executable, i.e. if you normally start Ultrastar with
```
ultrastardx -ConfigFile some_config.ini
```
you can instead use
```
/path/to/ultrastar-playback.py -ConfigFile some_config.ini
```
and it will work just the same. Thus, the script can serve as a drop-in replacement for calling the ```ultrastardx``` executable directly.

## Latency
The PulseAudio module-loopback contains a latency setting, which specifies the maximum latency in ms. This is currently set to the minimum value of 1 using a variable in the script. Lower values are more CPU intensive, however, I run Ultrastar on a relatively low-end mini PC and don't have any issues at all with CPU utilization. If you are encountering slowdowns, you could try raising the value.

### Audio Output
It is critical to note the the latency introduced by PulseAudio is not the only source of latency in your audio setup. If you're using HDMI audio output, the latency introduced by the audio equipment outside your PC is likely much, much higher. HDMI audio is notorious for high latency playback. In my setup, using HDMI output, the script provides a significant reduction in latency from Ultrastar's built-in microphone playback feature, but there is still a noticeable lag.

I strongly recommend that the script be used with analog audio output only. Before I play Ultrastar, I plug in a 3.5 mm audio cable to the output jack on my PC. PulseAudio switches to this output automatically, and I switch the input source on my AVR. Then, I start Ultrastar with the script. When paired with analog audio output, there is no perceivable lag at all in my setup. After I'm finished, I unplug the 3.5 mm cable, which switches the audio output back to HDMI.

## Volume Adjustment
With my microphones, the game is too loud by default and it is difficult to hear the singing over the music. Ultrastar Deluxe currently has no master volume setting. For a workaround, you can adjust the application volume with PulseAudio. With Ultrastar running, execute the following command:
```
pactl list sink-inputs
```

Find the sink input that that has ```ultrastardx``` as its ```application.name``` property. Take note of the sink input number. Then, adjust the volume using the ```set-sink-input-volume``` command. For example, in my case the sink input number is 5 and my desired volume is 80%, so the command is:
```
pactl set-sink-input-volume 5 80%
```
The volume adjustment will take effect immediately; it is not necessary to restart the application. Experiment with the volume until you find a satisfactory value. 

This only needs to be done once. The value will persist between sessions.

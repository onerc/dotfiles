## Audio tweaks
- Comment out `load-module module-suspend-on-idle` in `/etc/pulse/default.pa` because for some reasons sinks suspend and dont like to waking up
- Disable `Automatic Gain Control` of Discord so it doesn't mess up with volume and break the audio related stacks in the bar 
- Uncomment `flat-volumes = no` in `/etc/pulse/daemon.conf`. `rm -rf /etc/pulse/ ~/.pulse ~/.config/pulse` if it seems like it didnt work. I love pulseaudio.

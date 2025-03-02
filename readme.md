## Current setup 
qBittorrent theme: [DarkLight-qBittorent-WebUI](https://github.com/crash0verride11/DarkLight-qBittorent-WebUI)

Terminal font: [SFMono-Nerd-Font-Ligaturized](https://github.com/shaunsingh/SFMono-Nerd-Font-Ligaturized)

GTK theme: [Arc-BLACKEST](https://github.com/rtlewis88/rtl88-Themes/tree/Arc-BLACKEST)

Icon: [papirus-icon-theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

Cursor: [apple_cursor](https://github.com/ful1e5/apple_cursor)

~~## Audio tweaks~~
~~- Comment out `load-module module-suspend-on-idle` in `/etc/pulse/default.pa` because for some reason sinks suspend and dont like to waking up~~
~~- Disable `Automatic Gain Control` of Discord so it doesn't mess up with volume and break the audio related stacks in the bar~~
~~- Uncomment `flat-volumes = no` in `/etc/pulse/daemon.conf`. `rm -rf /etc/pulse/ ~/.pulse ~/.config/pulse` if it seems like it didnt work. I love pulseaudio.~~

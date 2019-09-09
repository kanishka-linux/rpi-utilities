## Instructions and scripts for installing kawaii-player on Raspberry Pi with some other miscellaneous scripts and configs.

### Making Raspberry Pi 4 (Debian Buster) into a casting device with [kawaii-player](https://github.com/kanishka-linux/kawaii-player)

1. `ssh` into Raspberry Pi (RPi) then execute following instructions for installing kawaii-player on it.

        $ git clone https://github.com/kanishka-linux/rpi-utilities
        $ cd rpi-utilities
        $ chmod +x rpiscript.py
        $ ./rpiscript.py
        
2. Note down local http address which will be printed on the terminal at the end of above step. It will be of the format `http://ip:port` (e.g. http://192.168.1.1:9001)
        
3. Disable `xcompmgr` on RPi using `raspi-config`, otherwise it will cause screen tearing when playing video.

4. Edit `/etc/dphys-swapfile` and increase swap value `CONF_SWAPSIZE=1024` 
   * Default swap value is 100, set this value to 1024. It is necessary for Rpi with 1 GB memory. 
   * For 2 GB or higher memory it is not required.
   
5. `$ sudo reboot` : reboot to see changes

6. Now install `kawaii-player` on any other computer with any OS (GNU/Linux, OSX or Windows). We'll call this computer `Master` PC.
   * Enable Media Server on the Master 
   * Set `Preferences`->`PC-To-PC Casting` -> `Master`, which will add new menu `PC To PC Casting` to the playlist context menu.
   * From the newly added context menu, setup `Slave IP Address` (i.e. add address of RPi which one has noted down in step 2).
   * Once slave ip addres has been setup on the master, one can cast any video/audio/playlist from master to Rpi, using the same context menu.
   * For more information on `PC-To-PC Casting` in the context of kawaii-player, take a look at this [link](https://github.com/kanishka-linux/kawaii-player/wiki/Casting) 
   
#### Any Advantage of using RPi and kawaii-player instead of regular casting device?

* [kawaii-player](https://github.com/kanishka-linux/kawaii-player) on Rpi 4 (with Debian Buster) uses [libmpv](https://github.com/mpv-player/mpv) as a playback engine. Hence it can play almost all formats without transcoding.
* Rpi 4 officially supports hardware decoding of HEVC/H.265 videos. It was able to play 10-bit HEVC videos without much of a problem (except heating issue - one needs to add heat sink or cooling fan to the RPi setup to deal with it).
* Cast local audio, local video, torrents, ytdl supported links and entire playlists from master to slave.
* Easily change audio/subtitle track during playback of mkv files. One can also add external subtitles on the fly.
* Good support for subtitle rendering (i.e. fonts, colors, border etc..) and color correction
* Precise seeking
* One can also use Rpi 4 + kawaii-player as a regular media server along with functionality as a casting device.
* Control master from mobile web interface, and instruct master to cast videos to slave. 

#### How to reinstall kawaii-player in case of some problems in the initial installation?
* Remove kawaii-player 
        
      $ sudo apt remove kawaii-player
      $ sudo apt autoremove
    
* Remove kawaii-player folder if present in the existing directory
      
      $ rm -rf kawaii-player/
    
* Remove config directory
      
      $ rm -rf ~/.config/kawaii-player

* Remove autostart file
      
      $ rm ~/.config/autostart/kawaii.desktop
    
* Remove (or backup) mpv config file
      
      $ rm ~/.config/mpv/config # removal
          OR
      $ mv ~/.config/mpv/config ~/.config/mpv/config.bak # backup
    
* Now repeat installation method as given in the 1st step.

#### More settings

* Edit `~/.config/kawaii-player/config.txt`, `~/.config/kawaii-player/other_options.txt` or `~/.config/kawaii-player/torrent_config.txt` and change player settings manually.
* Edit `~/.config/mpv/config` and modify mpv related options directly.
* After changing above files one needs to restart the application or simply reboot the RPi.
* Before changing config files manually, if possible backup the original. Wrong values can leave the application un-workable on the RPi.
* If you've mouse/keyboard attached to the RPi, then one can change settings from the GUI itself without directly fiddling with config files.

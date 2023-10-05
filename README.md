## Instructions and scripts for installing kawaii-player on Raspberry Pi with some other miscellaneous scripts and configs.

### Making Raspberry Pi 4 (with Debian Buster) into a casting device with [kawaii-player](https://github.com/kanishka-linux/kawaii-player)

1. `ssh` into Raspberry Pi (RPi) then execute following instructions for installing kawaii-player on it.

        $ git clone https://github.com/kanishka-linux/rpi-utilities
        $ cd rpi-utilities
        $ chmod +x rpiscript.py
        $ ./rpiscript.py
        
        with latest mpv on debian bullseye

        $ ./rpiscript mpv-latest
                
2. Note down local http address which will be printed on the terminal at the end of above step. It will be of the format `http://ip:port` (e.g. http://192.168.1.1:9001)
        
3. Disable `xcompmgr` on RPi using `raspi-config`, otherwise it will cause screen tearing when playing video.

4. Edit `/etc/dphys-swapfile` and increase swap value `CONF_SWAPSIZE=1024` 
   * Default swap value is 100, set this value to 1024. It is necessary for Rpi with 1 GB memory. 
   * For 2 GB or higher memory it is not required.
   
5. `$ sudo reboot` : reboot to apply changes

6. Now install [kawaii-player](https://github.com/kanishka-linux/kawaii-player#dependencies-and-installation) on any other computer (GNU/Linux, OSX or Windows). We'll call this computer `Master` PC, from which we'll cast videos to RPi
   * Enable Media Server on the Master 
   * Set `Preferences`->`PC-To-PC Casting` -> `Master`, which will add new menu `PC To PC Casting` to the playlist context menu.
   * From the newly added context menu, setup `Slave IP Address` (i.e. add address of RPi which one has noted down in step 2).
   * Once slave ip addres has been setup on the master, one can cast any video/audio/playlist from library of the master to Rpi, using the same context menu.
   * For more information on `PC-To-PC Casting` in the context of kawaii-player, visit this [link](https://github.com/kanishka-linux/kawaii-player/wiki/Casting) 
   
#### Any Advantage of using RPi and kawaii-player instead of regular casting device?

* [kawaii-player](https://github.com/kanishka-linux/kawaii-player) on RPi 4 (with Debian Buster) uses [libmpv](https://github.com/mpv-player/mpv) as a playback engine. Hence it can play almost all formats supported by mpv without requiring any kind of transcoding at the master or slave side.
* RPi 4 officially supports hardware decoding of HEVC/H.265 videos. It was able to play 10-bit HEVC videos without much of a problem (except heating issue - one needs to add heat sink or cooling fan to the RPi setup to deal with it). (latest version mpv/libmpv doesn't support proper hardware decoding on rpi using mmal, so support for libvlc has been added)
* Cast local audio, local video, torrents, ytdl supported links and entire playlists from master to slave.
* Easily change audio/subtitle track during playback of mkv files. One can also add external subtitles on the fly.
* Good support for subtitle rendering (i.e. fonts, colors, border etc..) and color correction
* Precise seeking
* One can also use RPi 4 + kawaii-player as a regular media server along with functionality as a casting device.
* Control master from mobile web interface, and instruct master to cast videos to slave. 

#### How to reinstall kawaii-player in case of some problems in the initial installation?
* Remove kawaii-player 
        
      $ sudo apt remove kawaii-player
      $ sudo apt autoremove

* if compton is installed

      $ sudo apt remove compton
      $ rm ~/.config/autostart/compton.desktop
    
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
* For tearfree experince with latest mpv (v0.35+) use only openbox (not mutter),  disable xcompmgr and install compton. 

#### Is it possible to install kawaii-player on RPi 3 models?

* Installing kawaii-player is not a problem on RPi 3. One can follow regular instructions as given in the [README](https://github.com/kanishka-linux/kawaii-player/blob/master/README.md) of the kawaii-player for installing it on debian/ubuntu based systems. 
* In RPi 3 models main problem is getting `mpv/libmpv` to work, with proper support for hardware decoding of videos. For this, one needs to update RPi firmware first and then needs to compile and install mpv from the source. Moreover there is no support for hardware decoding of H.265 videos. 
* If one is interested in the audio playback only then mpv available in the official repository is more than enough - which will be installed automatically during installation of kawaii-player.
* `libmpv` most probably won't work with kawaii-player and RPi 3, so users may need to use `mpv` binary to get the audio/video playback. For playing video, users may need to use `vo=rpi` in the mpv config file.

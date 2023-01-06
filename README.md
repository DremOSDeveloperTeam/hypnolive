# hypnolive

## Up-to-date Hypnospace pages from the internet!

Note: I plan on making this much more user-friendly later.

### Prerequisites
#### Windows
Look, I don't use Windows. I ran from it the second I had a chance. That said, this is the way I remember using Git.

* Hypnospace Outlaw (duh)
* [Git for Windows](https://gitforwindows.org/)
* [Python 3.10 or above](https://www.python.org/downloads/windows/)

#### Linux

* Hypnospace Outlaw (duh)
* Git (install from your package manager)
* Python 3.10 or above (install from your package manager)

### Installation
#### Windows

* Open Git BASH for Windows
* Go to Hypnospace Outlaw's mod folder in Windows Explorer - Usually C:\Users\[yourusername]\Tendershoot\HypnOS\mods\
* Right click, and click "Open Open with Git BASH" (or something like that)
* Clone this repository
 * Run: git clone https://github.com/Innovation/hypnolive
<!--* Clone this repository - git clone https://git.innovation-inc.org/Innovation/hypnolive-->

At this point, the mod will be made available in-game. Start the game!
* Click the "Mods" button on whatever save file you're going to use. Check "Hypnolive"
* Start the save file.

You will immediately have access to the Hypnolive zone. Welcome to Hypnolive!

#### Linux
##### **NOTE: This assumes you are running the Windows version of Hypnospace Outlaw through Proton. This is necessary if you plan to contribute to Hypnolive!**

* Open a terminal and go to Hypnospace Outlaw's mod folder - Usually ~/Tendershoot/HypnOS/mods/
 * If you use the Steam Flatpak, it'll be ~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/844590/pfx/drive_c/users/steamuser/Tendershoot/mods/
* Clone this repository
 * Run: git clone https://git.innovation-inc.org/Innovation/hypnolive

At this point, the mod will be made available in-game. Start the game!    
* Click the "Mods" button on whatever save file you're going to use. Check "Hypnolive"
* Start the save file.

You will immediately have access to the Hypnolive zone. Welcome to Hypnolive! 

### Updating
Eventually, this mod will keep itself up to date. However, during this experimental stage, it will require you to update it yourself.

#### Windows

* Open Git for Windows
* Go to Hypnospace Outlaw's mod folder - Usually C:\Users\[yourusername]\Tendershoot\HypnOS\mods\
* Pull the repository - git pull

The pages should automagically refresh when you restart HypnOS or the game.

#### Linux

* Go to Hypnospace Outlaw's mod folder - Usually ~/Tendershoot/HypnOS/mods/
* Pull the repository - git pull 

The pages should automagically refresh when you restart HypnOS or the game.

### Automatically Starting the Script

It may be more convenient to start the companion script when your computer starts. Here's how to do that.

#### Windows

I forgot how Windows services work...

#### Linux

* Create a new user systemd service file at /etc/systemd/user
 * $ nano $HOME/.config/systemd/user/hypnolive-companion.service
* Write the following text file (with appropriate changes):
```
[Unit]
Description=Hypnolive Companion
After=multi-user.target

[Service]
Type=simple
Restart=always
WorkingDirectory=/path/to/mods/hypnolive/
ExecStart=/usr/bin/python3 /path/to/companion.py

[Install]
WantedBy=multi-user.target
```

So, for most Non-Flatpak Installs:
```
[Unit]
Description=Hypnolive Companion
After=multi-user.target

[Service]
Type=simple
Restart=always
WorkingDirectory=%h/Tendershoot/HypnOS/mods/hypnolive/
ExecStart=/usr/bin/python3 %h/Tendershoot/HypnOS/mods/hypnolive/companion.py                                                                                                                                          

[Install]
WantedBy=multi-user.target
```

And most Flatpak Installs:
```

You may now start your new service with `systemctl --user status hypnolive-companion.service`, and make it start on bootup with `systemctl --user enable hypnolive-companion.service`.

[Unit]
Description=Hypnolive Companion
After=multi-user.target

[Service]
Type=simple
Restart=always
WorkingDirectory=%h/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/844590/pfx/drive_c/users/steamuser/Tendershoot/HypnOS/mods/hypnolive/
ExecStart=/usr/bin/python3 %h/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/844590/pfx/drive_c/users/steamuser/Tendershoot/HypnOS/mods/hypnolive/companion.py -d

[Install]
WantedBy=multi-user.target
```

### Contributing

Want your own Hypnospace pages on Hypnolive? Download the [offical development tools](https://jay-tholen.itch.io/hsps), and start making your own pages.

Fork the repository and make your changes according to the guide below.

Currently, the layout for pages is as follows:
```
hypnolive
|-hs
   |-69_Hypnolive
                |-[your username].hsp  <-- This serves as your main page. Additional pages should be placed in a directory with your username!
                |-[your username]      <-- The rest of your pages should be placed here!
                                |-bluhbluhbluh.hsp
```

When you're happy with your changes, make a pull request. I'll look it over and make sure it doesn't break anyone elses pages, as well as make sure there's nothing that would violate Hypnospace Law.

Later on, when I make a companion app, you'll also be able to add your own repositories if you want to skip the pull request process.

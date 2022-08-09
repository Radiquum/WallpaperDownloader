# Wallpaper Changer&Downloader

Python script for downloading daily bing wallpapers or windows spotlight wallpapers.
with possibility to set it as a wallpaper on Gnome (42).

thanks to [WinLight](https://github.com/Biswa96/WinLight) for already done implementation of windows spotlight download.

## How to use

1. Clone this repository `git clone https://github.com/Radiquum/WallpaperDownloader`
2. Install requirements.txt `python -m pip install -r requirements.txt`
3. double click or run `python WallpaperDownloader.py`

you can run it in background by using `nohup [Path to]/WallpaperDownloader.py -c ~/[Path to]/config.ini`

configuration can be found in `config.ini`

<!-- idk if this script can be scheduled to run by timer through [cron](https://en.wikipedia.org/wiki/Cron)
([crontab.guru](https://crontab.guru/)) -->

## License

WallpaperDownloader is licensed under the GNU General Public License v3. A full copy of the license is provided in [LICENSE](https://github.com/Radiquum/WallpaperDownloader/blob/master/LICENSE).

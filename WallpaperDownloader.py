import configparser
import os
from sys import platform

import requests
import xmltodict
from PIL import Image


"""

bing wallpaper history url
https://www.bing.com/HPImageArchive.aspx?format=xml&idx={page?}&n={1-7}&cc={market}

market - market code, default: en-US
available markets: https://docs.microsoft.com/en-us/bing/search-apis/bing-image-search/reference/market-codes#country-codes
markets with specific pictures available:

    US - United States (Default, used when no unique wallpaper is available)
    DE - Germany
    JP - Japan

    GB - United Kingdom
    NZ - New Zealand
    AU - Australia
    BR - Brazil
    FR - France
    CA - Canada
    ES - Spain
    IN - India
    CN - China


bing wallpaper url
https://bing.com/th?id={name}_{resolution}.jpg&qlt={quality}

can be any resolution or UHD for Ultra HD wallpapers
can be any quality, minimum recommended value is 30, set it to 100 for no compression

"""


config = configparser.ConfigParser()
if not os.path.isfile("config.ini"):
    config["DEFAULT"] = {
        ";only for bing\n" "market": "US",
        ";only for bing. spotlight resolution always 1920x1080 and 1080x1920\n"
        "resolution": "1920x1080",
        ";only for bing. spotlight quality is unknown\n" "quality": "50",
        ";download path, relative to current folder or to home folder (~)\n"
        "download_folder": "wallpapers",
        ";auto wallpaper update supported only on gnu\\linux with gnome (42) Desktop Environment.\n"
        ';Windows users can download "Dynamic Theme" app from Microsoft Store.\n'
        ";True or False\n"
        "update_wallpapers": "False",
        ";source can be either bing or windows_spotlight\n" "source": "bing",
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)
config.read("config.ini")
market: str = config["DEFAULT"]["market"]
resolution: str = config["DEFAULT"]["resolution"]
quality: str = config["DEFAULT"]["quality"]

download_folder = os.path.expanduser(config["DEFAULT"]["download_folder"])
update_wallpapers = config.getboolean("DEFAULT", "update_wallpapers")

source = config["DEFAULT"]["source"]


def get_bing_daily_wallpaper():
    response = requests.get(
        f"https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&cc={market}"
    )
    parsed = xmltodict.parse(response.text)["images"]
    url_base: str = parsed["image"]["urlBase"]

    wallpaper_url = f"https://bing.com{url_base}_{resolution}.jpg&qlt={quality}"
    file_name = f"{wallpaper_url.split('&')[0].split('=')[1]}"

    print(wallpaper_url)
    print(file_name)

    os.makedirs(download_folder, exist_ok=True)
    download_file(wallpaper_url, f"{download_folder}/{file_name}")
    write_metadata(f"{download_folder}/{file_name}", parsed)
    if update_wallpapers is True:
        set_wallpaper(f"{download_folder}/{file_name}")


def download_file(url, file_name):
    try:
        if os.path.exists(file_name):
            return True

        r = requests.get(url, stream=True)
        if r.status_code != 200:
            print(
                f'Got a HTTP {r.status_code} while downloading \
"{file_name}" ({url})'
            )
            return False
        with open(file_name, "wb") as file:
            for data in r.iter_content(chunk_size=1024):
                file.write(data)
    except KeyboardInterrupt:
        print("Finished downloading")
        os.remove(file_name)
        exit()
    return True


def write_metadata(file_name, parsed):
    image = Image.open(file_name)
    exif = image.getexif()

    artist = parsed["image"]["copyright"].split(" (")[1].strip("© ").strip(")")
    exif.update([(269, parsed["image"]["copyright"].split(" (")[0])])
    exif.update([(270, parsed["image"]["headline"])])

    exif.update([(306, parsed["image"]["fullstartdate"])])

    exif.update([(315, artist)])
    exif.update([(33432, artist)])

    image.save(file_name, exif=exif)


def set_wallpaper(file):
    file = f"file://{os.path.realpath(file)}"
    if platform in ["linux", "linux2"]:
        DE = os.environ.get("DESKTOP_SESSION")
        if DE in ["gnome", "gnome-xorg", "gnome-wayland"]:
            os.system(f"gsettings set org.gnome.desktop.background picture-uri {file}")
            os.system(
                f"gsettings set org.gnome.desktop.background picture-uri-dark {file}"
            )
        else:
            print("Desktop Environment is not supported")
    else:
        print("platform is not supported")


if __name__ == "__main__":
    if source == "bing":
        get_bing_daily_wallpaper()
    if source == "windows_spotlight":
        exec(open("WinLight.py").read())

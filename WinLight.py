#! /usr/bin/python
# https://github.com/Biswa96/WinLight/blob/master/WinLight.py
# Import modules
# sourcery skip: avoid-builtin-shadow
import fileinput
import os
import re

import requests

from WallpaperDownloader import download_folder
from WallpaperDownloader import set_wallpaper
from WallpaperDownloader import update_wallpapers


def download_spotlight():
    # Set environment variables
    ImageUrl = (
        "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData"
    )
    JsonFile = ".spotlight_cache.json"

    # JsonUrl="https://arc.msn.com/v3/Delivery/Placement?&fmt=json&cdm=1&ctry=US&pid=209567"
    JsonUrl = (
        "https://arc.msn.com/v3/Delivery/Placement?&fmt=json&cdm=1&ctry=US&pid=279978"
    )
    # JsonUrl="https://arc.msn.com/v3/Delivery/Placement?&fmt=json&cdm=1&ctry=US&pid=338380"
    # JsonUrl="https://arc.msn.com/v3/Delivery/Placement?&fmt=json&cdm=1&ctry=US&pid=338387"

    SearchPattern = r"(?<=imageFileData/).*?(?=\?ver)"
    HttpHeader = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "User-Agent": "WindowsShellClient/9.0.40929.0 (Windows)",
    }

    # Download JSON file
    Response = requests.get(JsonUrl, headers=HttpHeader)
    with open(JsonFile, "wb") as file:
        file.write(Response.content)

    # Remove back slashes
    for line in fileinput.input(JsonFile, inplace=True, encoding="utf-8"):
        print(line.replace("\\", "")),

    # Remove opening quotes
    for line in fileinput.input(JsonFile, inplace=True, encoding="utf-8"):
        print(line.replace('"{', "{")),

    # Remove closing quotes
    for line in fileinput.input(JsonFile, inplace=True, encoding="utf-8"):
        print(line.replace('}"', "}")),

    with open(JsonFile, encoding="utf-8") as file:
        content = file.read()

    # Get the hashes from links and download
    img_hash = re.findall(SearchPattern, content, re.DOTALL)

    if update_wallpapers is True:
        j = f"{ImageUrl}/{img_hash[00]}"
        os.makedirs(f"{download_folder}/spotlight", exist_ok=True)
        FileName = f"{download_folder}/spotlight/{img_hash[00]}.jpg"
        print(j)
        Response = requests.get(j, headers=HttpHeader)
        with open(FileName, "wb") as file:
            file.write(Response.content)

        set_wallpaper(f"{download_folder}/spotlight/{img_hash[00]}.jpg")
    else:
        # download all wallpapers from a page
        for i in img_hash:
            j = f"{ImageUrl}/{i}"
            os.makedirs(f"{download_folder}/spotlight", exist_ok=True)
            FileName = f"{download_folder}/spotlight/{i}.jpg"
            print(j)
            Response = requests.get(j, headers=HttpHeader)
            with open(FileName, "wb") as file:
                file.write(Response.content)
            # Delete files less that 2 KB which are blank
            if os.path.getsize(FileName) < 2048:
                os.remove(FileName)

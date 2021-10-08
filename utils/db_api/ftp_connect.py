import ftplib
import logging
import json
import os
from data.config import HOST_FTP, USER_FTP, PASSWORD_FTP

filename = "brands.json"


def return_brands_ftp(update):
    data_brands = None
    try:
        data_brands = load_file_json()
    except Exception as e:
        logging.info(e)
    finally:
        if data_brands is None and not update:
            update = True
    if update:
        ftp = ftplib.FTP(HOST_FTP)
        ftp.login(USER_FTP, PASSWORD_FTP)
        ftp.cwd('/scraper_settings')
        # Write file in binary mode
        with open(filename, "wb") as file:
            # Command for Downloading the file "RETR filename"
            ftp.retrbinary(f"RETR {filename}", file.write)
        ftp.quit()
        data_brands = load_file_json()
    # FTP_list = ftp.nlst()
    return data_brands


def update_brands_db():
    with open(filename, "rb") as file:
        # use FTP's STOR command to upload the file
        ftp = ftplib.FTP(HOST_FTP)
        ftp.login(USER_FTP, PASSWORD_FTP)
        ftp.cwd('/scraper_settings')
        ftp.storbinary(f"STOR {filename}", file)


def add_brand_name_in_bd(name_brand: str):
    data_bd = load_file_json()
    if name_brand in data_bd:
        return None
    data_bd.append(name_brand)
    save_file_json(data_bd)
    # update in ftp
    update_brands_db()


def delete_brand_in_bd(name_brand: str):
    data_bd = load_file_json()
    if name_brand not in data_bd:
        return None
    data_bd.remove(name_brand)
    save_file_json(data_bd)
    # update in ftp
    update_brands_db()


def load_file_json():
    with open(f'{os.getcwd()}/brands.json', 'r', encoding='utf-8') as file:
        new_value = json.load(file)
    return new_value


def save_file_json(value):
    with open(f'{os.getcwd()}/brands.json', 'w', encoding='utf-8') as file:
        json.dump(value, file, indent=4, ensure_ascii=False)

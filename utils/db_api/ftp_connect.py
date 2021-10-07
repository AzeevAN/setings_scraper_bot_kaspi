import ftplib
import json
import logging

from data.config import HOST_FTP, USER_FTP, PASSWORD_FTP, load_file_json

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

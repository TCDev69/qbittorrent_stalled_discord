import os
import sys
import time
import logging
import qbittorrentapi as qbittorrentapi
import datetime as dt
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime

#################################################
webhook_url = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxx' #Discord webhook
id = 'xxxxxxxxxxxxxxxxxx'    #Discord username ID
qhost="http://localhost/",   #Qbittorrent ip
qport=int("8080"),           #Qbittorrent port
quser="admin",               #Qbittorrent username
qpass="adminadmin",          #Qbittorrent password
#################################################

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=int('20'),
        datefmt='%Y-%m-%d %H:%M:%S')

def fix_stalled():
    try:
        logging.info("--- START fix_stalled START ---")
        conn_info = dict(
            host=qhost,
            port=int(qport),
            username=quser,
            password=qpass,
        )
        logging.info("Connecting...")
        qbt_client = qbittorrentapi.Client(**conn_info)

        decrease_prio(qbt_client, qbt_client.torrents.info(status_filter="stalled_downloading"))
        decrease_prio(qbt_client, qbt_client.torrents.info(status_filter="active"))

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error("%s %s %s", exc_type, fname, exc_tb.tb_lineno, exc_info=1)
    finally:
        logging.info("--- END fix_stalled END ---")
          

def decrease_prio(qbt_client, data):
    for torrent in data:
        logging.info("Torrent: %s", torrent.info.hash)
        logging.info("      - hash:        %s", torrent.info.hash)
        logging.info("      - state:       %s", torrent.info.state)
        logging.info("      - num_seeds:   %s", torrent.info.num_seeds)
        logging.info("      - time_active: %s", str(dt.timedelta(seconds=torrent.info.time_active)))
        if torrent.state == 'stalledDL' and torrent.info.time_active > 300:
            logging.info("      - action: %s", "setting bottom priority")
            qbt_client.torrents.bottom_priority(torrent_hashes=torrent.hash)
            
            hook = DiscordWebhook(url=webhook_url, content="File Stopped<@!{}>".format(id))
            embed = DiscordEmbed(title="Torrent Stalled", color=0xf8c1b8)
            embed.add_embed_field(name='Torrent', value=torrent.info.hash)
            embed.set_footer(text=str(dt.timedelta(seconds=torrent.info.time_active)))
            embed.set_timestamp()
            hook.add_embed(embed)
            hook.execute()
            
        elif torrent.state == 'metaDL' and torrent.info.num_seeds == 0 and torrent.info.time_active > 300:
            logging.info("      - action: %s", "setting bottom priority")
            qbt_client.torrents.bottom_priority(torrent_hashes=torrent.hash)
            
            hook = DiscordWebhook(url=webhook_url, content="File Stopped<@!{}>".format(id))
            embed = DiscordEmbed(title="Can't download metadata", color=0xf8c1b8)
            embed.add_embed_field(name='Torrent', value=torrent.info.hash)
            embed.set_footer(text=str(dt.timedelta(seconds=torrent.info.time_active)))
            embed.set_timestamp()
            hook.add_embed(embed)
            hook.execute()
            
        elif torrent.state == 'downloading' and torrent.info.num_seeds == 0 and torrent.info.time_active > 1800:
            logging.info("      - action: %s", "setting bottom priority")
            qbt_client.torrents.bottom_priority(torrent_hashes=torrent.hash)
            
            hook = DiscordWebhook(url=webhook_url, content="File Stopped<@!{}>".format(id))
            embed = DiscordEmbed(title="No seeders", color=0xf8c1b8)
            embed.add_embed_field(name='Torrent', value=torrent.info.hash)
            embed.set_footer(text=str(dt.timedelta(seconds=torrent.info.time_active)))
            embed.set_timestamp()
            hook.add_embed(embed)
            hook.execute()
            
        else:
            logging.info("      - action: %s", "nothing")

while True:
    fix_stalled()
    time.sleep(150)

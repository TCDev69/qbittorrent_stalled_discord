# Stalled Torrents

When a torrent stalled it automatically decrease his priority and send an embed using a webhook to Discord

## Setup:
### Change line 11-16
```py
#################################################
webhook_url = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxx'
id = 'xxxxxxxxxxxxxxxxxx'
qhost="http://localhost/",   //Qbittorrent ip
qport=int("8080"),           //Qbittorrent port
quser="admin",               //Qbittorrent username
qpass="adminadmin",          //Qbittorrent password
#################################################
```
### Install requirements
```
pip3 install -r requirements.txt
```
### Change username
Open the file with `nano ./stall.service` and change `/home/USERNAME` (use /root/ if user = root) 
```
ExecStart=/usr/bin/python3 /home/USERNAME/stall.py
```
## Move the file `main.py` into ~/
```sh
mv ./main.py ~/
```

## Run on startup:
```
sudo cp ./stall.service /etc/systemd/system/stall.service
systemctl enable stall.service
```

## Run
### From systemctl:
```
systemctl start stall.service
```

### From terminal:
```
python3 ~/main.py
```

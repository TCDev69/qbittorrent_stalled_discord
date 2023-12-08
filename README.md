# Stalled Torrents

When a torrent stalled it automatically decrease his priority and send an embed using a webhook to Discord

## Setup:
### change line 11-16
```py
#################################################
webhook_url = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxx'
id = 'xxxxxxxxxxxxxxxxxx'
qhost="http://localhost/",
qport=int("8080"),
quser="admin",
qpass="adminadmin",
#################################################
```
### install requirements
```sh
sh ./reqs.sh
```

## Run on startup:
```sh
cp ./stall.service /etc/systemd/system/stall.service
systemctl enable stall.service
```

## Run
### from systemctl:
```
systemctl start stall.service
```

### from terminal:
```sh
python3 main.py
```

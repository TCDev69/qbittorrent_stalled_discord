# Stalled Torrents

When a torrent stalled it automatically decrease his priority and send an embed using a webhook to Discord

## Setup:
### Change line 11-16
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
### Install requirements
```
sh ./reqs.sh
```

## Run on startup:
```
cp ./stall.service /etc/systemd/system/stall.service
systemctl enable stall.service
```

## Run
### From systemctl:
```
systemctl start stall.service
```

### From terminal:
```
python3 main.py
```

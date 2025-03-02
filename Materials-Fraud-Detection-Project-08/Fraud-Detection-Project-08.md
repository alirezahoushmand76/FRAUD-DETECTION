## Setup the smtp section in `grafana.ini` file

Go to this URL:

🚩 https://myaccount.google.com/

1.  You should activate two step verification first.
2.  Then go to Security>App Password and generate one for you.
3.  Copy and Paste these 16-digit in the following snippet 

```bash
enabled = true
host = smtp.gmail.com:587
user = WRITE-YOUR-GMAIL-HERE
password = PUT-YOUR-APP-PASS-HERE
skip_verify = true
from_address = WRITE-YOUR-GMAIL-HERE
from_name = Grafana
```

## Config `grafana.ini` file in docker container

Go to `grafana:/etc/grafana` and copy `garfana.ini` file to your desktop. After editing the file, uplod it again into grafana container by the following command(s):

```bash
docker cp ./grafana.ini grafana:/etc/grafana

docker restart grafana
```

### Get the SSH key and `chmod` it 

```bash
chmod 400 YOUR-KEY.pem

ssh -i ~/.ssh/YOUR-KEY.pem ubuntu@5.34.193.57
```

### `mkdir` a directory and change its ownership

```bash
mkdir grafana-storage

sudo chown -R 472:472 ./grafana-storage
#472 is the default user of Grafana
```

###  Install docker on your server (from IRAN 🤔)

```bash
sudo snap install docker

sudo bash -c 'cat > /var/snap/docker/current/config/daemon.json <<EOF
{
  "insecure-registries" : ["https://docker.arvancloud.ir"],
  "registry-mirrors": ["https://docker.arvancloud.ir"]
}
EOF'

sudo snap restart docker

sudo docker run hello-world
```

**A good approach for installing Docker. But not from IRAN.** 

🛑 https://get.docker.com/

### Copy files between local and cloud

```bash
#from local machine to VM on the cloud
scp -i ~/.ssh/ar-fp-privatekey.pem -r cloud  ubuntu@5.34.193.57:/home/ubuntu/docker-stack

#from vm to local
scp -i ~/.ssh/ar-fp-privatekey.pem ubuntu@5.34.193.57:/home/ubuntu/local/docker-compose.yaml /mnt/c/Users/fozou/Desktop/dc.yaml
```

### Check if a port of your VM is open or not

```bash
telnet 5.34.194.119 9092
```


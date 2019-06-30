# install docker on Debian

### dependencies for docker
```
sudo apt-get -y install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common 
```
### Install Docker's official GPG key:
```
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | sudo apt-key add -
```

### Check that the GPG fingerprint of the Docker key you downloaded matches the expected value:
```
sudo apt-key fingerprint 0EBFCD88
```

### Add the stable Docker repository:
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")    $(lsb_release -cs) stable"
```

### Install docker
```
sudo apt-get update
sudo apt-get -y install docker-ce
```

### Configure Docker to run as a non-root user:
```
sudo usermod -aG docker $USER
```

### Exit the shell and SSH to the VM again

### Confirm docker is installed correctly and confirm that you can run Docker as a non-root user
``` 
docker run hello-world
```
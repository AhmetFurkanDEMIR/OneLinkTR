![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=black) ![](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

# [OneLinkTR.com](https://onelinktr.com/)

![Screenshot_2022-07-06_14-57-58](https://user-images.githubusercontent.com/54184905/177545000-a5e9db3d-f489-4c4f-a123-987667b1d8d9.png)

**Keep It Together!**
With this application developed by the [SoftForRange](https://softforrange.com/) team, keep both your links and your customers together.

**Economize**
Don't have to allocate a separate ad budget for each app, get it all done at once!

**Application Logic**
Different market links of your application in different operating systems are combined and a single link is created, when the user goes to this link, the operating system is automatically detected and directed to the specific link for that operating system.

[**You can use OneLinkTR application right now and create a single link!!**](https://onelinktr.com/)

OR, you can run this application in your local by following the steps below.

### Deploying OneLinkTR with Docker.

![index](https://user-images.githubusercontent.com/54184905/177587011-5fc7947b-fa34-4cf3-95dd-78e90752de1d.jpeg)

In order to run the OneLinkTR application on our computer, we need to install Docker, we go to the link for Docker installation. [Link](https://docs.docker.com/engine/install/ubuntu/)

After the Docker installation, you need to install git on your computer so that you can pull the project to your own computer, run the command below to install git.

```terminal
sudo apt-get install git
```

Now that we have Git installed, we can pull the project to our local.

```terminal
git clone https://github.com/AhmetFurkanDEMIR/OneLinkTR
```

After we pull the project to our local, we need to make some changes specific to your computer. 

First of all, create a yadex mail so that you can verify mail in the application, then go to the Python script file called [PyScripts/tools.py](/PyScripts/tools.py) and enter your yandex account information in the "MyEmail" and "MyEmailPass" variables, so you can send verification links via smtp with your yandex account.

```python
global MyEmail
global MyEmailPass
MyEmail = "your_yandex_mail"
MyEmailPass = "your_password"
```

After completing the mail operations, we need to make some changes and configurations to direct the project from docker to our public ip address.

Run the following Python code on your Ubuntu computer and find out your computer's public ip address.

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()
```

In this example my ip address is "192.168.1.33", it should give you an ip address like this, now you need to paste the ip address into the "myIp" variable in the Python script called [PyScripts/tools.py](/PyScripts/tools.py).

```python
ServerPort = 5000
global myUrl
myIp = "192.168.1.33"
myUrl = "http://{}:{}/".format(str(myIp), str(ServerPort))
```

We have created a url with our public ip, and thanks to this url, we will be able to verify user accounts. 

After these operations, we will create a docker network with this public address, edit and run the following command according to your own ip address to create the network.

```terminal
docker network create -o "com.docker.network.bridge.host_binding_ipv4"="192.168.1.33" bridge2
```

Now that we have finished all our configuration processes, we can deploy the images in the [docker-compose.yml](/docker-compose.yml) file and access our application.

We have two images in the docker-compose.yml file.

The first image contains the PostgreSQL database. When we deploy this image, the sql commands in [sql/create_tables.sql](/sql/create_tables.sql) are run and the necessary tables are created.

In the second image, we have our website that we wrote with Python-Flask, when this image is deployed, the python packages in [requirements.txt](/requirements.txt) are loaded and then the application is deployed on the public ip.

Run the following command to deploy these two images and access the application.

```terminal
# Cleaning up Docker images
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

# Running all images (While in the project folder)
sudo docker-compose up -d
```

Now that our images are deployed, you can access the OneLinkTR application via http://YourPublicIp:5000. (my Url: http://192.168.1.33:5000/)




#### Contributors

* [Ahmet Furkan DEMIR](https://www.ahmetfurkandemir.com/)

* [Mustafa Esen](https://www.linkedin.com/in/mustafa-esen-6a1546194/)

* [SoftForRange](https://softforrange.com/)

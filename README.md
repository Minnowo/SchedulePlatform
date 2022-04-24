# UniSurvival

## About

- Python docstring format: Google

## Dependencies

### Backend Dependencies - Python packages (`requirements.txt`)

- [fastapi](https://github.com/tiangolo/fastapi) >= 0.75.1
- [uvicorn](https://www.uvicorn.org/) >= 0.17.6
- [requests](https://docs.python-requests.org/en/latest/) >= 2.26.0
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) >= 8.0.27
- [icalendar](https://github.com/collective/icalendar) >= 4.0.9

pip quick setup with: `$ pip install -r requirements.txt` from within the same directory.

## Ubuntu Server Setup

### Ubuntu MySQL DB and user setup

*Note: '#' denotes comments.*

**Warning: The following instructions are a unsafe for production as it gives single users mass access to DBs and
tables!**

```
sudo apt-get install mysql-server

sudo mysql_secure_installation utility

sudo ufw reset
sudo ufw enable
sudo ufw allow mysql

sudo systemctl start mysql  # start mysql service
sudo systemctl enable mysql  # run mysql service continuously

cd /etc/mysql/mysql.conf.d
sudo nano mysqld.cnf  # change bind address to 0.0.0.0

sudo systemctl restart mysql  # restart mysql service

# Get your PUBLIC IPV4 Address of the machine you want to connect to the SQL server with.

sudo mysql -u root -p

CREATE DATABASE fooDatabase;
CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';  # try without ‘ ‘ if it doesn’t work
GRANT ALL ON fooDatabase.* TO ‘fooUser’@’fooPublicIpv4Address’; 
GRANT ALL ON fooDatabase.* TO ‘fooUser’@’%’; 
GRANT ALL ON *.* TO 'new_user'@'localhost’;  # try without ‘ ‘ if it doesn’t work
FLUSH PRIVILEGES;

sudo systemctl restart mysql  # restart mysql service
```

### Ubuntu Server & MySQL DB timezone setup

*Note: The MySQL DB should be running on the UTC timezone*

1. Check server timezone: `$ cat /etc/timezone`
2. Change server timezone: `$ sudo timedatectl set-timezone America/Toronto`
3. Check MySQL timezone: `$ sudo mysql -e "SELECT @@global.time_zone;"`
4. Change MySQL timezone: `$ sudo mysql -e "SET GLOBAL time_zone = ‘-5:00’;"` or `mysql > SET time_zone = '+8:00'`

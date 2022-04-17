# UniSurvival

## About

- Python docstring format: Google

## Ubuntu server & MySQL DB timezone setup

**Note: The MySQL DB should be running on the UTC timezone**

1. Check server timezone: `$ cat /etc/timezone`
2. Change server timezone: `$ sudo timedatectl set-timezone America/Toronto`
3. Check MySQL timezone: `$ sudo mysql -e "SELECT @@global.time_zone;"`
4. Change MySQL timezone: `$ sudo mysql -e "SET GLOBAL time_zone = ‘-5:00’;"` or `mysql > SET time_zone = '+8:00'`

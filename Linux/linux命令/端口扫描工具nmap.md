# [https://github.com/nmap/nmap](https://github.com/nmap/nmap)

- [https://nmap.org/](https://nmap.org/)

```bash
wget https://nmap.org/dist/nmap-7.91.tar.bz2
bzip2 -cd nmap-7.91.tar.bz2 | tar xvf -
cd nmap-7.91
yum install gcc gcc-c++
./configure
make -j4
make install
```

```bash
# 获取基本信息
nmap www.baidu.com
Starting Nmap 7.91 ( https://nmap.org ) at 2020-10-29 12:21 CST
Warning: File ./nmap-services exists, but Nmap is using /usr/local/bin/../share/nmap/nmap-services for security and consistency reasons.  set NMAPDIR=. to give priority to files in your local directory (may affect the other data files too).
Nmap scan report for www.baidu.com (14.215.177.38)
Host is up (0.0017s latency).
Other addresses for www.baidu.com (not scanned): 14.215.177.39
Not shown: 998 filtered ports
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 9.76 seconds
# -O: Enable OS detection
nmap -O 192.168.137.129
# -A: Enable OS detection, version detection, script scanning, and traceroute
nmap -A 192.168.137.129
```

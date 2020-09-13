### [Nodemailer](https://github.com/andris9/Nodemailer)是一个简单易用的Node.js邮件发送组件。
```nodejs
var nodemailer = require('nodemailer');

// create reusable transporter object using SMTP transport
var transporter = nodemailer.createTransport({
    'host': 'smtp.163.com',
    'port': 465,
    'secure': true,
    auth: {
        user: 'yourname@163.com',
        pass: 'password'
    }
});

// setup e-mail data with unicode symbols
var mailOptions = {
    from: 'from@163.com', // sender address
    to: 'to@qq.com', // list of receivers
    subject: 'Hello', // Subject line
    text: 'Hello world ', // plaintext body
    html: '<b>Hello world </b>' // html body
};

// send mail with defined transport object
transporter.sendMail(mailOptions, function(error, info){
    if(error){
        return console.log(error);
    }
    console.log('Message sent: ' + info.response);
});
```
如果不知道smtp服务器可以查找[services.json](https://github.com/andris9/nodemailer-wellknown/blob/master/services.json)使用简写，如service: '163'。
###[发送附件](https://github.com/andris9/Nodemailer#attachments)
```nodejs
var mailOptions = {
    ...
    attachments: [
        {   // utf-8 string as an attachment
            filename: 'text1.txt',
            content: 'hello world!'
        },
        {   // file on disk as an attachment
            filename: 'text2.txt',
            path: '/path/to/file.txt' // stream this file
        }
    ]
}
```
### 常用端口
- 25端口（SMTP）：25端口为SMTP（Simple Mail Transfer
Protocol，简单邮件传输协议）服务所开放的，是用于发送邮件。
- 109端口（POP2）：109端口是为POP2（Post Office Protocol Version
2，邮局协议2）服务开放的，是用于接收邮件的。
- 110端口（POP3）：110端口是为POP3（Post Office Protocol Version
3，邮局协议3）服务开放的，是用于接收邮件的。
- 143端口（IMAP）：143端口是为IMAP（INTERNET MESSAGE ACCESS PROTOCOL）服务开放的，是用于接收邮件的。
####基于SSL（SecureSockets Layer安全套接层）协议的安全的邮件收发协议。
- 465端口（SMTPS）：465端口是为SMTPS（SMTP-over-SSL）协议服务开放的，这是SMTP协议基于SSL安全协议之上的一种变种协议，它继承了SSL安全协议的非对称加密的高度安全可靠性，可防止邮件泄露。SMTPS和SMTP协议一样，也是用来发送邮件的，只是更安全些，防止邮件被黑客截取泄露，还可实现邮件发送者抗抵赖功能。防止发送者发送之后删除已发邮件，拒不承认发送过这样一份邮件。
- 995端口（POP3S）：995端口是为POP3S（POP3-over-SSL）协议服务开放的，这是POP3协议基于SSL安全协议之上的一种变种协议。
- 993端口（IMAPS）：993端口是为IMAPS（IMAP-over-SSL）协议服务开放的，这是IMAP协议基于SSL安全协议之上的一种变种协议。
### 参照：

- [https://github.com/andris9/Nodemailer](https://github.com/andris9/Nodemailer)
- [邮件服务端口 port 25、109、110、143、465、995、993](http://www.douban.com/note/397681162/)


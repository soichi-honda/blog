## /var/log/mailog
### re(ceiver@sugasugasugaya.ml
```
Aug 14 04:07:36 ip-172-31-24-156 postfix/smtpd[3711]: 3F1B7C0C918: client=localhost[127.0.0.1]
Aug 14 04:07:36 ip-172-31-24-156 postfix/cleanup[3714]: 3F1B7C0C918: message-id=<20200814040736.3F1B7C0C918@postfix-test.ml>
Aug 14 04:07:36 ip-172-31-24-156 postfix/qmgr[3104]: 3F1B7C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:07:38 ip-172-31-24-156 postfix/smtp[3715]: 3F1B7C0C918: to=<re(ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[18.204.191.21]:587, delay=2.5, delays=0.1/0.01/1.5/0.87, dsn=2.0.0, status=sent (250 Ok 01000173eb26d8c0-1c8e57ef-ebe0-4bbf-90dd-937e2ee5726e-000000)
Aug 14 04:07:38 ip-172-31-24-156 postfix/qmgr[3104]: 3F1B7C0C918: removed
```

### re)ceiver@sugasugasugaya.ml
```
Aug 14 04:11:13 ip-172-31-24-156 postfix/smtpd[3711]: 74F80C0C918: client=localhost[127.0.0.1]
Aug 14 04:11:13 ip-172-31-24-156 postfix/cleanup[3723]: 74F80C0C918: message-id=<20200814041113.74F80C0C918@postfix-test.ml>
Aug 14 04:11:13 ip-172-31-24-156 postfix/qmgr[3104]: 74F80C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:11:15 ip-172-31-24-156 postfix/smtp[3724]: 74F80C0C918: to=<re)ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[18.204.191.21]:587, delay=2.4, delays=0.15/0.01/1.4/0.86, dsn=2.0.0, status=sent (250 Ok 01000173eb2a28ed-c74cb833-decc-4f2e-9026-93e30914b5a8-000000)
Aug 14 04:11:16 ip-172-31-24-156 postfix/qmgr[3104]: 74F80C0C918: removed
```

### re<ceiver@sugasugasugaya.ml
```
Aug 14 04:13:05 ip-172-31-24-156 postfix/smtpd[3711]: 55223C0C918: client=localhost[127.0.0.1]
Aug 14 04:13:05 ip-172-31-24-156 postfix/cleanup[3726]: 55223C0C918: message-id=<20200814041305.55223C0C918@postfix-test.ml>
Aug 14 04:13:05 ip-172-31-24-156 postfix/qmgr[3104]: 55223C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:13:07 ip-172-31-24-156 postfix/smtp[3727]: 55223C0C918: to=<re<ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[18.235.65.23]:587, delay=2.5, delays=0.12/0.01/1.5/0.89, dsn=2.0.0, status=sent (250 Ok 01000173eb2bde4e-b8c0e7cc-9ee5-4bb8-b28b-32e501d8f883-000000)
Aug 14 04:13:07 ip-172-31-24-156 postfix/qmgr[3104]: 55223C0C918: removed
```

### re>ceiver@sugasugasugaya.ml
```
Aug 14 04:15:46 ip-172-31-24-156 postfix/smtpd[3711]: D79F5C0C918: client=localhost[127.0.0.1]
Aug 14 04:15:47 ip-172-31-24-156 postfix/cleanup[3730]: D79F5C0C918: message-id=<20200814041546.D79F5C0C918@postfix-test.ml>
Aug 14 04:15:47 ip-172-31-24-156 postfix/qmgr[3104]: D79F5C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:15:48 ip-172-31-24-156 postfix/smtp[3731]: D79F5C0C918: to=<re>ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[3.93.117.106]:587, delay=2.1, delays=0.34/0.01/1.4/0.34, dsn=5.0.0, status=bounced (host email-smtp.us-east-1.amazonaws.com[3.93.117.106] said: 501 Invalid RCPT TO address provided (in reply to RCPT TO command))
Aug 14 04:15:49 ip-172-31-24-156 postfix/bounce[3732]: D79F5C0C918: sender non-delivery notification: 3AD3CC0C919
```

### re\>ceiver@sugasugasugaya.ml
```
Aug 14 04:46:26 ip-172-31-24-156 postfix/smtpd[3866]: 49D67C0C918: client=localhost[127.0.0.1]
Aug 14 04:46:26 ip-172-31-24-156 postfix/cleanup[3878]: 49D67C0C918: message-id=<20200814044626.49D67C0C918@postfix-test.ml>
Aug 14 04:46:26 ip-172-31-24-156 postfix/qmgr[3104]: 49D67C0C918: from=<sender@postfix-test.ml>, size=381, nrcpt=1 (queue active)
Aug 14 04:46:28 ip-172-31-24-156 postfix/smtp[3880]: 49D67C0C918: to=<re>ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.193.82.158]:587, delay=1.9, delays=0.11/0.01/1.4/0.34, dsn=5.0.0, status=bounced (host email-smtp.us-east-1.amazonaws.com[34.193.82.158] said: 501 Invalid RCPT TO address provided (in reply to RCPT TO command))
Aug 14 04:46:28 ip-172-31-24-156 postfix/bounce[3881]: 49D67C0C918: sender non-delivery notification: 73DC1C0C919
Aug 14 04:46:28 ip-172-31-24-156 postfix/qmgr[3104]: 49D67C0C918: removed
```

### re[ceiver@sugasugasugaya.ml
```
Aug 14 04:16:44 ip-172-31-24-156 postfix/smtpd[3711]: A97BAC0C918: client=localhost[127.0.0.1]
Aug 14 04:16:44 ip-172-31-24-156 postfix/cleanup[3730]: A97BAC0C918: message-id=<20200814041644.A97BAC0C918@postfix-test.ml>
Aug 14 04:16:44 ip-172-31-24-156 postfix/qmgr[3104]: A97BAC0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:16:47 ip-172-31-24-156 postfix/smtp[3731]: A97BAC0C918: to=<re[ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[3.93.117.106]:587, delay=2.4, delays=0.14/0/1.4/0.87, dsn=2.0.0, status=sent (250 Ok 01000173eb2f36b6-fb077c76-9e75-4fe8-98ad-ef4bef7953a8-000000)
Aug 14 04:16:47 ip-172-31-24-156 postfix/qmgr[3104]: A97BAC0C918: removed
```

### re]ceiver@sugasugasugaya.ml
```
Aug 14 04:17:35 ip-172-31-24-156 postfix/smtpd[3711]: 913C9C0C918: client=localhost[127.0.0.1]
Aug 14 04:17:35 ip-172-31-24-156 postfix/cleanup[3730]: 913C9C0C918: message-id=<20200814041735.913C9C0C918@postfix-test.ml>
Aug 14 04:17:35 ip-172-31-24-156 postfix/qmgr[3104]: 913C9C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:17:38 ip-172-31-24-156 postfix/smtp[3731]: 913C9C0C918: to=<re]ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.200.200.58]:587, delay=2.5, delays=0.13/0/1.5/0.87, dsn=2.0.0, status=sent (250 Ok 01000173eb2ffdf7-aa0d2bd1-34eb-4b0d-b04a-36b743764508-000000)
Aug 14 04:17:38 ip-172-31-24-156 postfix/qmgr[3104]: 913C9C0C918: removed
```

### re:ceiver@sugasugasugaya.ml
```
Aug 14 04:18:48 ip-172-31-24-156 postfix/smtpd[3711]: BE1B4C0C918: client=localhost[127.0.0.1]
Aug 14 04:18:48 ip-172-31-24-156 postfix/cleanup[3730]: BE1B4C0C918: message-id=<20200814041848.BE1B4C0C918@postfix-test.ml>
Aug 14 04:18:48 ip-172-31-24-156 postfix/qmgr[3104]: BE1B4C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:18:50 ip-172-31-24-156 postfix/smtp[3731]: BE1B4C0C918: to=<re:ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[54.156.166.64]:587, delay=2.2, delays=0.11/0/1.4/0.71, dsn=5.0.0, status=bounced (host email-smtp.us-east-1.amazonaws.com[54.156.166.64] said: 554 Transaction failed: Address contains illegal characters in user name: '<"re:ceiver"@sugasugasugaya.ml>'. (in reply to end of DATA command))
Aug 14 04:18:51 ip-172-31-24-156 postfix/bounce[3777]: BE1B4C0C918: sender non-delivery notification: 26FCBC0C919
Aug 14 04:18:51 ip-172-31-24-156 postfix/qmgr[3104]: BE1B4C0C918: removed
```

### re;ceiver@sugasugasugaya.ml
```
Aug 14 04:21:24 ip-172-31-24-156 postfix/smtpd[3711]: 4F989C0C918: client=localhost[127.0.0.1]
Aug 14 04:21:24 ip-172-31-24-156 postfix/cleanup[3789]: 4F989C0C918: message-id=<20200814042124.4F989C0C918@postfix-test.ml>
Aug 14 04:21:24 ip-172-31-24-156 postfix/qmgr[3104]: 4F989C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:21:26 ip-172-31-24-156 postfix/smtp[3790]: 4F989C0C918: to=<re;ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[100.24.109.150]:587, delay=2.5, delays=0.12/0.01/1.4/0.99, dsn=2.0.0, status=sent (250 Ok 01000173eb337b1e-9166b69a-825e-40ed-b5a5-73af942d5be0-000000)
Aug 14 04:21:26 ip-172-31-24-156 postfix/qmgr[3104]: 4F989C0C918: removed
```

### re,ceiver@sugasugasugaya.ml
```
Aug 14 04:22:54 ip-172-31-24-156 postfix/smtpd[3711]: 1E3D2C0C918: client=localhost[127.0.0.1]
Aug 14 04:22:54 ip-172-31-24-156 postfix/cleanup[3789]: 1E3D2C0C918: message-id=<20200814042254.1E3D2C0C918@postfix-test.ml>
Aug 14 04:22:54 ip-172-31-24-156 postfix/qmgr[3104]: 1E3D2C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:22:56 ip-172-31-24-156 postfix/smtp[3790]: 1E3D2C0C918: to=<re,ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.201.255.191]:587, delay=2.7, delays=0.32/0/1.4/0.99, dsn=2.0.0, status=sent (250 Ok 01000173eb34da70-7515bb8f-56cb-4e9a-bf85-6bbe535c0ce7-000000)
Aug 14 04:22:56 ip-172-31-24-156 postfix/qmgr[3104]: 1E3D2C0C918: removed
```

### re@ceiver@sugasugasugaya.ml
```
Aug 14 04:23:29 ip-172-31-24-156 postfix/smtpd[3711]: 9147CC0C918: client=localhost[127.0.0.1]
Aug 14 04:23:29 ip-172-31-24-156 postfix/cleanup[3789]: 9147CC0C918: message-id=<20200814042329.9147CC0C918@postfix-test.ml>
Aug 14 04:23:29 ip-172-31-24-156 postfix/qmgr[3104]: 9147CC0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:23:31 ip-172-31-24-156 postfix/smtp[3790]: 9147CC0C918: to=<re@ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.192.72.77]:587, delay=2.2, delays=0.13/0/1.4/0.71, dsn=5.0.0, status=bounced (host email-smtp.us-east-1.amazonaws.com[34.192.72.77] said: 554 Transaction failed: Address contains illegal characters in user name: '<"re@ceiver"@sugasugasugaya.ml>'. (in reply to end of DATA command))
Aug 14 04:23:31 ip-172-31-24-156 postfix/bounce[3792]: 9147CC0C918: sender non-delivery notification: F24FFC0C919
Aug 14 04:23:31 ip-172-31-24-156 postfix/qmgr[3104]: 9147CC0C918: removed
```

### re\ceiver@sugasugasugaya.ml
```
Aug 14 04:24:14 ip-172-31-24-156 postfix/smtpd[3711]: 9B2C5C0C918: client=localhost[127.0.0.1]
Aug 14 04:24:14 ip-172-31-24-156 postfix/cleanup[3789]: 9B2C5C0C918: message-id=<20200814042414.9B2C5C0C918@postfix-test.ml>
Aug 14 04:24:14 ip-172-31-24-156 postfix/qmgr[3104]: 9B2C5C0C918: from=<sender@postfix-test.ml>, size=374, nrcpt=1 (queue active)
Aug 14 04:24:16 ip-172-31-24-156 postfix/smtp[3790]: 9B2C5C0C918: to=<receiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[52.54.2.148]:587, delay=2.4, delays=0.12/0/1.4/0.88, dsn=2.0.0, status=sent (250 Ok 01000173eb36143e-d6e2e3c5-8a25-48f7-8d2d-526be5089f8a-000000)
Aug 14 04:24:17 ip-172-31-24-156 postfix/qmgr[3104]: 9B2C5C0C918: removed
```
### re\\ceiver@sugasugasugaya.ml
```
Aug 14 04:33:20 ip-172-31-24-156 postfix/smtpd[3711]: E0903C0C918: client=localhost[127.0.0.1]
Aug 14 04:33:22 ip-172-31-24-156 postfix/cleanup[3809]: E0903C0C918: message-id=<20200814043320.E0903C0C918@postfix-test.ml>
Aug 14 04:33:22 ip-172-31-24-156 postfix/qmgr[3104]: E0903C0C918: from=<sender@postfix-test.ml>, size=382, nrcpt=1 (queue active)
Aug 14 04:33:24 ip-172-31-24-156 postfix/smtp[3810]: E0903C0C918: to=<re\ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.200.141.115]:587, delay=3.9, delays=1.6/0.01/1.4/0.83, dsn=2.0.0, status=sent (250 Ok 01000173eb3e702d-e13e6372-90ab-4ce7-a20d-421e3099f852-000000)
Aug 14 04:33:24 ip-172-31-24-156 postfix/qmgr[3104]: E0903C0C918: removed
```

### .receiver@sugasugasugaya.ml
```
Aug 14 04:24:51 ip-172-31-24-156 postfix/smtpd[3711]: 2B1D9C0C918: client=localhost[127.0.0.1]
Aug 14 04:24:51 ip-172-31-24-156 postfix/cleanup[3789]: 2B1D9C0C918: message-id=<20200814042451.2B1D9C0C918@postfix-test.ml>
Aug 14 04:24:51 ip-172-31-24-156 postfix/qmgr[3104]: 2B1D9C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:24:53 ip-172-31-24-156 postfix/smtp[3790]: 2B1D9C0C918: to=<.receiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[23.23.95.169]:587, delay=2.5, delays=0.12/0/1.4/0.94, dsn=2.0.0, status=sent (250 Ok 01000173eb36a338-32bfd563-da65-49a1-9133-a6d700505044-000000)
Aug 14 04:24:53 ip-172-31-24-156 postfix/qmgr[3104]: 2B1D9C0C918: removed
```

### receiver.@sugasugasugaya.ml
```
Aug 14 04:25:33 ip-172-31-24-156 postfix/smtpd[3711]: 54331C0C918: client=localhost[127.0.0.1]
Aug 14 04:25:33 ip-172-31-24-156 postfix/cleanup[3789]: 54331C0C918: message-id=<20200814042533.54331C0C918@postfix-test.ml>
Aug 14 04:25:33 ip-172-31-24-156 postfix/qmgr[3104]: 54331C0C918: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 14 04:25:35 ip-172-31-24-156 postfix/smtp[3790]: 54331C0C918: to=<receiver.@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[34.192.117.72]:587, delay=2.3, delays=0.11/0/1.4/0.86, dsn=2.0.0, status=sent (250 Ok 01000173eb3747a5-a09eeea7-c142-4fb5-9b28-69d980037d29-000000)
Aug 14 04:25:35 ip-172-31-24-156 postfix/qmgr[3104]: 54331C0C918: removed
```

### re..ceiver@sugasugasugaya.ml
```
Aug 14 04:26:11 ip-172-31-24-156 postfix/smtpd[3711]: CC98EC0C918: client=localhost[127.0.0.1]
Aug 14 04:26:11 ip-172-31-24-156 postfix/cleanup[3789]: CC98EC0C918: message-id=<20200814042611.CC98EC0C918@postfix-test.ml>
Aug 14 04:26:11 ip-172-31-24-156 postfix/qmgr[3104]: CC98EC0C918: from=<sender@postfix-test.ml>, size=382, nrcpt=1 (queue active)
Aug 14 04:26:14 ip-172-31-24-156 postfix/smtp[3790]: CC98EC0C918: to=<re..ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[3.226.144.129]:587, delay=2.3, delays=0.12/0/1.4/0.85, dsn=2.0.0, status=sent (250 Ok 01000173eb37ddff-dfc1b704-279b-4f2e-a609-f801f9603d46-000000)
```

### re'ceiver@sugasugasugaya.ml
```
Aug 14 04:29:22 ip-172-31-24-156 postfix/smtpd[3711]: 470B4C0C918: client=localhost[127.0.0.1]
Aug 14 04:29:22 ip-172-31-24-156 postfix/cleanup[3796]: 470B4C0C918: message-id=<20200814042922.470B4C0C918@postfix-test.ml>
Aug 14 04:29:22 ip-172-31-24-156 postfix/qmgr[3104]: 470B4C0C918: from=<sender@postfix-test.ml>, size=376, nrcpt=1 (queue active)
Aug 14 04:29:24 ip-172-31-24-156 postfix/smtp[3797]: 470B4C0C918: to=<re'ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[52.207.66.31]:587, delay=2.3, delays=0.12/0/1.4/0.85, dsn=2.0.0, status=sent (250 Ok 01000173eb3ac5eb-22ceba44-95d3-4087-8d48-0460c8110842-000000)
Aug 14 04:29:24 ip-172-31-24-156 postfix/qmgr[3104]: 470B4C0C918: removed
```
### re\"ceiver@sugasugasugaya.ml
```
Aug 14 04:30:13 ip-172-31-24-156 postfix/smtpd[3711]: 0CDD4C0C918: client=localhost[127.0.0.1]
Aug 14 04:30:13 ip-172-31-24-156 postfix/cleanup[3796]: 0CDD4C0C918: message-id=<20200814043013.0CDD4C0C918@postfix-test.ml>
Aug 14 04:30:13 ip-172-31-24-156 postfix/qmgr[3104]: 0CDD4C0C918: from=<sender@postfix-test.ml>, size=382, nrcpt=1 (queue active)
Aug 14 04:30:15 ip-172-31-24-156 postfix/smtp[3797]: 0CDD4C0C918: to=<re"ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[3.231.236.85]:587, delay=2.4, delays=0.12/0/1.4/0.86, dsn=2.0.0, status=sent (250 Ok 01000173eb3b8c66-82620bfa-de90-46b7-94af-042fa2f79daf-000000)
Aug 14 04:30:15 ip-172-31-24-156 postfix/qmgr[3104]: 0CDD4C0C918: removed
```

### re ceiver@sugasugasugaya.ml
```
Aug 18 04:25:53 ip-172-31-24-156 postfix/smtpd[2639]: CA4B9C0C91F: client=localhost[127.0.0.1]
Aug 18 04:25:53 ip-172-31-24-156 postfix/cleanup[2642]: CA4B9C0C91F: message-id=<20200818042553.CA4B9C0C91F@postfix-test.ml>
Aug 18 04:25:53 ip-172-31-24-156 postfix/qmgr[2379]: CA4B9C0C91F: from=<sender@postfix-test.ml>, size=380, nrcpt=1 (queue active)
Aug 18 04:25:56 ip-172-31-24-156 postfix/smtp[2643]: CA4B9C0C91F: to=<re ceiver@sugasugasugaya.ml>, relay=email-smtp.us-east-1.amazonaws.com[52.205.70.65]:587, delay=2.5, delays=0.12/0.03/1.4/0.91, dsn=2.0.0, status=sent (250 Ok 01000173ffd10812-caf8079b-1541-41bc-a19a-9b2156a43023-000000)
Aug 18 04:25:56 ip-172-31-24-156 postfix/qmgr[2379]: CA4B9C0C91F: removed
Aug 18 04:26:21 ip-172-31-24-156 postfix/smtpd[2639]: disconnect from localhost[127.0.0.1]
```

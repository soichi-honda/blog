## エラーについて
RHEL8 でタイムゾーンを変更しようとしたら、エラーが...

```bash
$ sudo timedatectl set-timezone Asia/Tokyo
Failed to set time zone: Failed to update /etc/localtime
```

## 原因

〇2020/12/10追記(ビューア様にコメントをいただきました)---

このエラーは、**セキュリティアップデートをおこなっていない RHEL8.2** でのみ起こる現象です。

[1779098 – SELinux prevents timedatex from searching the /etc/selinux/targeted/contexts/files directory](https://bugzilla.redhat.com/show_bug.cgi?id=1779098)

\---

[こちら](https://github.com/cockpit-project/bots/issues/78) もあわせて見たところ、SELinux がタイムゾーンの変更を禁止しているらしい。

実際に環境の SELinux の設定を確認してみると、たしかに SELinux が有効になってました。

```bash
$ getenforce
Enforcing
```

## 解決方法

〇2020/12/10追記(ビューア様にコメントをいただきました)---

RHEL8.2 のセキュリティアップデートをしてください!

アップデート後にタイムゾーンを変更すると、SELinux が有効でも問題なくコマンドが通るそうです。

\---

※これ以降の方法は **非推奨** となります。セキュリティアップデートが何らかの理由でできない、もしくはおこなっても解決しない場合に試してください。

SELinux を *Permissive* モード(*1)にしましょう。

\*1. *Permissive* モード  
SELinux ポリシーは強制されませんが、システムが動作し続けるため、AVC メッセージをログに記録し続けてくれます。  
SELinux を無効にしてしまうと、 AVC メッセージがログに出力されなくなってしまうので、基本的にこちらのモードを採用すべきだと思われます。

参考: [SELinux の使用 Red Hat Enterprise Linux 8 \| Red Hat Customer Portal](https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/8/html-single/using_selinux/index#changing-to-permissive-mode_changing-selinux-states-and-modes)

---

Permissive モードに変更する前に前提条件を確認します。。

```bash
$ sudo yum list installed |grep selinux-policy-targeted
$ sudo yum list installed |grep libselinux-utils
$ sudo yum list installed |grep policycoreutils
```

---

問題なければ SELinux のモードを変更します。

```bash
$ sudo cp -a /etc/selinux/config /etc/selinux/config.org
$ sudo ls /etc/selinux/config.org
$ sudo vi /etc/selinux/config
---
SELINUX=enforcing
→ SELINUX=permissive
---
$ sudo diff /etc/selinux/config /etc/selinux/config.org
$ getenforce //確認
```

---

この状態で再度タイムゾーンを変更してみます。

```bash
$ sudo timedatectl set-timezone Asia/Tokyo
$ sudo timedatectl status
               Local time: Wed 2020-12-02 17:28:58 JST
~省略~
```

いけました！


## 変更履歴
- 2020/12/10 内容追記&修正 ビューア様にいただいたコメントをもとに内容を変更しています。
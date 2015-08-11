## Raspberry Piって?
* Raspberry pi 財団が開発したカード型コンピュータ
* 標準OSにはLinuxを採用
* パソコンの基本的な動作の理解と、初歩的なプログラミングスキルの習得を促進することを目的としている
* $20～$35 という、Linuxが動作するパソコンとしては破格の値段で一気に普及

## 各部の名称と役割
モデルによって多少差はあるが、基本的には同じと考えてよい
* SoC
* GPU
* USB端子
* コンポジット出力
* ヘッドホン出力
* HDMI出力
* Ethernet
* 電源用microUSB
* GPIO
* カメラ端子
* ディスプレイ端子

## Raspberry Pi と Arduino の違い
基本的には以下の理解で問題ないと思われる

**Raspberry Pi → パソコン**

**Arduino → マイコン**

### Raspberry pi の特徴
* シングルボードコンピュータ
* パソコンの基本的な動作の理解と、初歩的なプログラミングスキルの習得を促進することを目的に開発
* Linuxがそのまま動く
* USB、LAN、オーディオ、ディスプレイとパソコンに求められる端子類は標準搭載
    * 機能拡張は基本的にこの範囲で行う
* (パソコンとしては)安い($20～)
* 派生品は公式のラインナップに存在するもののみ
    * 非公式でBanana Piという模造品が存在する

### Arduino の特徴
* ワンボードマイコン
* 制御用マイコンのプロトタイピングを安価に行うことを目的に開発された経緯を持つ
* スケッチ(Arduinoを動かすためのプログラム一式)に書いてあることしかできない
* デジタル入出力とアナログ入力に対応したGPIOを搭載
* (入出力が一通り揃ったワンボードマイコンとしては)安い(約$22～)
* マイコンでありながらWeb言語からの制御に対応
* “シールド” と呼ばれる基板による機能拡張が容易
    * 逆に言うとシールドによる機能拡張が無いと使えないデバイスが多い(Ethernetとかヘッドホン端子とか)
* 回路図が公開されているため、公式・非公式合わせて派生品が多く存在する
    * オープンソースハードウェア

## Raspberry Pi の導入
### 必要なもの
* Raspberry Pi本体
* SDカード(4GB以上推奨)
* USB接続のキーボード
* 同上 マウス
* HDMIもしくはコンポジット入力に対応したモニタ(テレビ)
* スマートフォン用ACアダプタ(microUSB - AC電源)
    * 1.2A以上の出力に対応したものを推奨
    * USB電源コネクタ+microUSBケーブルでも代用可
* Raspbian OSのイメージファイル
* 上記を書き込むためのパソコン

### 使うまでの手順
* OSのイメージファイルをダウンロードする
* OSのイメージファイルをSDカードに書き込む
* SDカードをRaspberry Piに挿入する
* キーボード、マウス、ディスプレイをRaspberry Piに取り付ける
* スマートフォン用ACアダプタをRaspberry Piに取り付ける
* ACアダプタを電源プラグに差し込む
    * 差し込むと同時にRaspberry Piの電源が投入される
* Raspberry Pi本体のLEDが点灯していることと、画面にRaspberry Piからの出力がされていることを確認する
* 画面の表示に従い、Raspberry Piの初期設定を行う
   * このとき "Expand FileSystem" は必ず行っておくこと(SDカードの容量をフルに使用できるようになるため)
   * 設定し忘れた項目があっても以下のコマンドを入力することで、再び設定することができる

      `sudo raspi-config`

## Raspberry Piをネットワークに繋ぐ
### 有線LANでつなぐ場合
* LANケーブルを用意する
* 用意したLANケーブルをRaspberry PiのEthernetポートに接続する
* LANケーブルの何もつながっていない方をネットワークスイッチもしくはルーターの空いているEthernetポートに接続する
* EthernetポートのLEDの状態を確認し、ネットワークに接続できているかどうかを確認する
* `ifconfig` よりDHCPもしくは静的IPアドレスでネットワークに接続できていることを確認する

### 無線LANでつなぐ場合
* 予め接続する無線LANアクセスポイントのSSIDとパスワードをメモしておく
* USB接続の無線LANドングルを用意する
    * 使用しているOSのディストリビューションによっては対応していないもの有るので注意
* 無線LANドングルをRaspberry PiのUSBポートに差し込む
* 無線LANドングルがRaspberry Piに認識されているかを `lsusb` コマンドで確かめる
  (下記のコマンド出力のうち、一番下が無線LANアダプタ)

~~~
    pi@raspberrypi ~ $ lsusb
    Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp.
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.
    Bus 001 Device 004: ID 2019:ab2a PLANEX GW-USNano2 802.11n Wireless Adapter [Realtek RTL8188CUS]
~~~

* 無線LANの設定を`/etc/wpa_supplicant/wpa_supplicant.conf` ファイルより編集する
    * このとき接続するSSIDのパスフレーズの内容を平文で書き込みたくない場合は、事前に`wpa_passphase <SSID> <元々のパスフレーズ>` コマンドを実行しておき、暗号化したパスフレーズを出力しておくとよい

~~~
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    network={
        ssid=(SSID)
        proto=WPA2
        key_mgmt=WPA-PSK
        psk=(パスフレーズ)
    }
~~~

* 無線LANのインタフェースを一度 `sudo ifdown wlan0` で停止させてから `sudo ifup wlan0` で再び起動させる
    * 設定の再読み込みを行うため
* `ifconfig` よりDHCPもしくは静的IPアドレスでネットワークに接続できていることを確認する

## Raspberry Pi を他のパソコンから接続する
### SSHで接続する
* Raspberry pi の電源を入れる
* Raspberry pi がネットワークに接続されるまで待つ
* ネットワークに接続されたらSSHコマンドもしくはSSHクライアントでRaspberry piに以下のIDとパスワードで接続する
    * IPアドレス: 自身で設定したIPアドレス
    * ポート番号: 22
    * ID: pi
    * Password: raspberry

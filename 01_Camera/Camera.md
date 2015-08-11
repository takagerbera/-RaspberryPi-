## Raspberry pi にWebカメラを繋ぐ
### 作業を始める前に
* Raspberry Piのパッケージリストを更新する

   `sudo apt-get update`

### USBカメラを繋ぐ
* Raspberry pi のUSBポートにUSBカメラを繋ぐ
* `lsusb` コマンドを実行し、カメラが認識されているかどうか調べる

### USBカメラで画像を撮影する(fswebcam編)
* 以下のコマンドで `fswebcam` をインストールする

    `sudo aptiude install fswebcam`

* コマンドでUSBカメラで写真を撮影する

    `sudo fswebcam ./photo.jpg`

* 撮影した画像をSFTP経由で確認する

* (応用編) `fswebcam` にオプションを付けて撮影してみよう

    `sudo fswebcam <オプション> ./photo.jpg`

    * -p <Name>: イメージフォーマット
        * PNG、JPEG、GREY、YUVV
    * -r <dimentions>: 解像度
        * 320x240、480x320、640x480、1024x768、1280x720
    * --no-banner: バナーをOFFに
    * -F <frames>: 露光するフレーム数
        * 1 ～ 100
    * --rotate <angle>: 画像の回転
        * 0、90、180、270

参考: http://manpages.ubuntu.com/manpages/lucid/man1/fswebcam.1.html

### USBカメラで画像を撮影する(motion編)
* 以下のコマンドで `motion` をインストール

    `sudo aptiude install motion`

* 設定ファイル ` /etc/motion/motion.conf` を以下のように編集

    * width → 640
    * height → 480
    * output_normal → off
    * ffmpeg_cap_new → off
    * webcam_quality → 100
    * webcam_localhost → off
    * control_localhost → off

* 以下のコマンドでUSBカメラを使ったキャプチャを開始する

    `sudo motion`

    * もし起動時に"pidファイルが作れない"的なメッセージが出たら以下のコマンドを実行する

        `sudo mkdir /var/run/motion`

* キャプチャの模様を以下のURLから確認する

    http://(Raspberry PiのURL):8081

* (応用編) キャプチャの設定を以下のURLから変更してみる

    http://(Raspberry PiのURL):8080

## Raspberry PiでLED点灯(通称Lチカ)をしてみる

### 用意するもの
物品名 | 個数  
---|---
ブレッドボード | 1  
ジャンパーワイヤー(オス-メス) | 2
ジャンパーワイヤー(オス-オス) | 1
赤色LED | 1
抵抗 | 1

### GPIO って?
* General Purpose Input Outputの略で、汎用的な入出力に使われるインタフェースのこと
* 基本的にピン1本単位で制御を行い、ピンに対して電力がかかっているかどうかで1か0かを判断する
* 対象のピンが入力と出力のどちらであるかは事前に設定する
* ピンから出力される電圧/入力可能な電圧はハードによって異なるので、GPIOを使用する際は必ず仕様書(データシート)を確認すること
    * 入力可能な電圧以上の入力を加えると破損の可能性があるため

### Raspberry PiのGPIO

* GPIOの電圧は3.3V
* ピンアサインは旧モデルと新モデルで多少異なる
    * 旧モデル(Model A/Model B) : https://www.raspberrypi.org/documentation/usage/gpio/
    * 新モデル(Model A+/Model B+/Pi2) : https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/

### 部品を配置しよう
今回は出力ピンに18番、グランド(アース)のピンにその右隣を使用する(下の設置例はRaspberry Pi Model Bの場合)

![](https://gist.github.com/takagerbera/fd335beb0fc9a6b187bd/raw/6e2b8dccda3b04209a4e6320c7aeb0c83cf46b66/raspberry_pi_led_switching.png)

配置の際には次のことに注意すること
* プラスとマイナスを間違えないこと
    * LEDにもアノード(正極)とカソード(負極)という極性があるので注意(足が長いほうがアノード、短いほうがカソード)
* 抵抗はLEDに過電流が流れないよう、LEDの手前に設置する
    * 定格以上の電流を流した場合、LEDが壊れる可能性がある

### シェルでLチカしてみよう
* 18番ピンを使用することを宣言
    `sudo echo 18 > /sys/class/gpio/export`
* 18番ピンを出力に設定
    `sudo echo out > /sys/class/gpio/gpio18/direction`
* 18番ピンをONにする
    `sudo echo 1 > /sys/class/gpio18/value`
* 18番ピンをOFFにする
    `sudo echo 0 > /sys/class/gpio18/value`

### スクリプトでLチカしてみよう
今回はRaspberry Piに標準で入っているPythonの実行環境で簡単なサンプルを作ります。

#### 手順
* 予め部品をRaspberry Piならびにブレッドボードに取り付ける(上記参考)
* エディタでスクリプトファイルを作成(ここでは名前を `led_sample.py` とする)
* 作成したスクリプトファイルに対して以下のコマンドで実行権限を与える
    `chmod +x led_sample.py`
* 以下のコマンドでスクリプトファイルを実行する
    `sudo python led_sample.py`
* 終了する際はキーボードから `Ctrl+C` を入力する

#### コード
別途添付している `led_sample.py` を参照

#### スクリプト解説
まず最初に必要なパッケージ、モジュール類を使えるように定義します。
今回はRaspberry Piの制御パッケージ `RPi` と、時間制御の `time` の二つを使います
```python
# RPiパッケージからGPIOモジュールをインポート
# as はそのファイルで使う際の呼び名を決める
import RPi.GPIO as GPIO
# timeパッケージをインポート
import time
```

次にGPIOを使う際のおまじないとして次の二行を加えます。
```python
# GPIOを使う前のおまじない
# GPIO.BCM はチップベンダのBroadcom用のピンアサインを示している
GPIO.setmode(GPIO.BCM)
# 警告を無効化
GPIO.setwarning(False)
```

次の使用するGPIOピンの状態を決めてあげます。
複数本のピンに対して設定する場合は、ピンの本数ぶん定義を書く必要があります。
```python
# port はGPIOのピン番号を表す整数
port = 18
# GPIOの状態を設定
# GPIO.OUTは指定した番号のピンを出力に設定する
GPIO.setup(port, GPIO.OUT)
```

続いてLEDを点灯消灯させるためのループ文を書きます。
以下のループでは1秒点灯→1秒消灯→1秒点灯→...と繰り返しています。
sleep文に指定する整数値が大きければ大きいほど点灯もしくは消灯している時間が長くなります。
```python
# Lチカをするための無限ループ
while True:
    # 指定したピンの電圧をハイにする = LED ON
    GPIO.output(port, 1)
    # 1秒停止
    time.sleep(1)
    # 指定したピンの電圧をローにする = LED OFF
    GPIO.output(port, 0)
    # 1秒停止
    time.sleep(1)
```

プログラムの最後にはGPIOの状態をリセットするための一文を書きます。
これを行わないと、GPIOの状態がプログラムによって操作された後の状態のままになります。
```python
# GPIOの状態を元に戻すための命令
GPIO.cleanup()
```

参考: https://www.raspberrypi.org/learning/quick-reaction-game/worksheet/

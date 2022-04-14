# pysesame

pythonからWebAPIを介してSESAME4を操作するモジュール。  
Control SESAME4 by python. This module using Sesame4 WebAPI.

SESAME4はCANDY HOUSE, Inc.の製品です。  
SESAME4 is product of CANDY HOUSE, Inc.

SESAME4 Page:<https://jp.candyhouse.co/products/sesame4>  
SESAME WebAPI:<https://doc.candyhouse.co/ja/SesameAPI>  

## インストール(install)

```sh
git clone https://github.com/takagi-aki/pysesame
python3 -m pip install -r pysesame/requirements.txt
```

## 利用方法(usage)

### コマンドから(How to use on commandline)

#### 準備(initialize)

```sh
python3 -m pysesame init
```

pysesame_key.jsonが生成されるのでUUIDやキーを入力する。  
(It genarate file named 'pysesame_key.json'.
Next, you open file and set uuid and api_keys.)

#### 実行(execute)

```sh
python3 -m pysesame lock
python3 -m pysesame unlock
python3 -m pysesame get_log --page 1 --lg 5
```

### pythonから(How to use on python)

#### 初期化方法1(initialize 1)

```py
from pysesame import Sesame

my_sesame = Sesame(uuid = 'XXXX-XXX-XXX',
                   api_key = 'XXXXXXXXXX',
                   secret_key = 'XXXXXXXXXXX'):
```

#### 初期化方法2(initialize 2)

```py
from pysesame import Sesame

my_sesame = Sesame(file_path = 'example.json'):
```

#### ドアの施錠、解除、切り替え(lock,unlock and toggle doorlock)

```py
my_sesame.lock()
my_sesame.unlock()
my_sesame.toggle()
```

#### 状態の取得、ログの取得(get status and log)

```py
my_sesame.get_status()
my_sesame.get_log()
```

# pysesami

pythonからWebAPIを介してSESAMI4を操作するモジュール。  
Control SESAMI4 by python. This module using Sesami4 WebAPI.

SESAMI4はCANDY HOUSE, Inc.の製品です。  
SESAMI4 is product of CANDY HOUSE, Inc.

SESAMI4 Page:<https://jp.candyhouse.co/products/sesame4>  
SESAMI WebAPI:<https://doc.candyhouse.co/ja/SesameAPI>  

## インストール(install)

```sh
git clone https://github.com/takagi-aki/pysesami
python3 -m pip install -r pysesami/requirements.txt
```

## 利用方法(usage)

### コマンドから(How to use on commandline)

#### 準備(initialize)

```sh
python3 -m pysesami init
```

pysesami_key.jsonが生成されるのでUUIDやキーを入力する。  
(It genarate file named 'pysesami_key.json'.
Next, you open file and set uuid and api_keys.)

#### 実行(execute)

```sh
python3 -m pysesami lock
python3 -m pysesami unlock
python3 -m pysesami get_log --page 1 --lg 5
```

### pythonから(How to use on python)

#### 初期化方法1(initialize 1)

```py
from pysesami import Sesami

my_sesami = Sesami(uuid = 'XXXX-XXX-XXX',
                   api_key = 'XXXXXXXXXX',
                   secret_key = 'XXXXXXXXXXX'):
```

#### 初期化方法2(initialize 2)

```py
from pysesami import Sesami

my_sesami = Sesami(file_path = 'example.json'):
```

#### ドアの施錠、解除、切り替え(lock,unlock and toggle doorlock)

```py
my_sesami.lock()
my_sesami.unlock()
my_sesami.toggle()
```

#### 状態の取得、ログの取得(get status and log)

```py
my_sesami.get_status()
my_sesami.get_log()
```

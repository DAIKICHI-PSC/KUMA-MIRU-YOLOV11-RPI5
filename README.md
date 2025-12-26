「ＫＵＭＡ　ＭＩＲＵ］  
<img src="https://github.com/DAIKICHI-PSC/KUMA-MIRU-YOLOV11-RPI5/blob/main/materials/sample_pictures/detection0.jpg"> </img>  
<img src="https://github.com/DAIKICHI-PSC/KUMA-MIRU-YOLOV11-RPI5/blob/main/materials/sample_pictures/detection1.jpg"> </img>  
<img src="https://github.com/DAIKICHI-PSC/KUMA-MIRU-YOLOV11-RPI5/blob/main/materials/sample_pictures/detection2.jpg"> </img>  
  
---
  
「ＫＵＭＡ　ＭＩＲＵ」のyolov11（ncnn）バージョンです（Paspberry Pi5でOpenVINO版を使用するとメモリーリークが発生しハングアップします）。  
https://github.com/DAIKICHI-PSC/KUMA-MIRU  
Paspberry Pi5用に調整しました。  
Paspberry Pi5は低コストで、低消費電力なシステムです。  
GPU無しでも、非常に高速に動作します。  
詳細については、「ＫＵＭＡ　ＭＩＲＵ」を確認して下さい。  
運用の詳細については、各プログラムのコメントを確認して下さい。  
  
---
  
ターミナルでPythonの仮想環境を作成して下さい。  
python -m venv venv  
ターミナルでPythonの仮想環境を作有効にします。  
source venv/bin/activate
必要なモジュールをインストールします。  
pip install opencv-python  
pip install ultralytics  
  
ネットワークが無い環境は、「AIR-Stick WiFi（株式会社ニッチカンパニー社）」等を使用して下さい。  
電源が無い環境では、ソーラーバッテリーを使用して下さい。  
rootのパスワードを設定して下さい。  
リモートで管理する場合は、オープンソースのネットワークソフトウェア、SoftEther VPNを使用して下さい（ https://www.vpnazure.net/ja/ https://kone-life.com/367/ ）。  
SoftEther VPNの管理は、SoftEtherのサーバー管理ツール、Pi-Appsからbox86・box64・wineをインストールして下さい（4Kページサイズカーネルへ切り替えて下さい）。  
管理マネージャー接続例１：cd vpnsmgr  
管理マネージャー接続例２：wine vpnsmgr.exe  
ブリッジはeth1を指定して下さい。  
Paspberry Pi5のRealVNCを有効にし、Paspberry Pi5にリモート接続出来る様にして下さい（接続先は192.168.43.2になるかと思います）。  
ソフトウェアの起動をbashで自動化して下さい。  
記述例１：source venv/bin/activate  
記述例２：cd KUMA-MIRU-YOLOV11-RPI5  
記述例３：python kuma_miru.py  

---

［ライセンス］  
本プログラム  
AGPL3.0 LISENCE  
商用利用する場合は、Ultralytics社と商用利用ライセンス契約をするか、全てのソールコードを一般公開して下さい。  
  
yolov11  
AGPL3.0 LISENCE  
商用利用する場合は、Ultralytics社と商用利用ライセンス契約をするか、全てのソールコードを一般公開して下さい。  

---

［appreciation（感謝）］  
Inventor of yolov11  
ultralytics and the community  
https://github.com/ultralytics  

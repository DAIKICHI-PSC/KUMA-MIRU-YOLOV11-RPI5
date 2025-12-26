#====================================================================
#本プログラムは、AIで「熊」を検出するプログラムです（cocoデータセットの他の番号に変えれば、他の物体も高精度に検出可能です）。
#最近の熊による被害に対して、何か貢献出来ないかと思い、作成しました。
#物体検出結果を保持する変数external_outputを使用し、値によって外部出力して下さい（各種通知、パトライト等の熊への威嚇装置）。
#
#多方向の物体検出を安価に行う為、一台のPCに複数のWEBカメラを接続して運用出来る様にしました。
#十分な処理速度を保てる範囲で、複数台のカメラを接続して下さい（実際の運用ではリアルタイムで検出する必要はないので、６台程度までカメラを接続しても問題ないかと思います）。
#xrdpをインストールすれば、リモートで管理出来ます。
#オープンソースのネットワークソフトウェア、SoftEther VPNを使用する事で、柔軟なネットワークを使用した運用管理が可能になるのではないでしょうか。
#
#環境設定
#必要に応じて、設定ファイル「settings.txt」を編集して下さい（本プログラムのテストは、カメラを熊の画像に向けるか、検出する物体の番号を、熊の21から0にして人を検出してください）。。
#ウィンドウズのMicrosoft StoreよりPythonを検索し、最新版をインストールして下さい。
#コマンドプロントで、pip install opencv-pythonを実行してください。
#コマンドプロントで、pip install ultralyticsを実行してください。
#コマンドプロントで、pip install torchを実行してください。
#コマンドプロントで、pip install torchvisionを実行してください。
#コマンドプロントで、pip install torchaudioを実行してください。
#bashを使用して、自動起動出来るようにして下さい。
#
#Ultralytics社のモジュールを使用する事で、簡単にncnnを使用した、高速な物体検出が可能となりました。
#本プログラムはUltralytics社のモジュールと学習済みデータを使用します（データもAGPL3.0）。
#https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt をダウンロードして、本プログラムと同じフォルダに保存してく下さい。
#https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt をダウンロードして、本プログラムと同じフォルダに保存してく下さい。
#https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt をダウンロードして、本プログラムと同じフォルダに保存してく下さい。
#https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11l.pt をダウンロードして、本プログラムと同じフォルダに保存してく下さい。
#https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt をダウンロードして、本プログラムと同じフォルダに保存してく下さい。
#
#ライセンス
#AGPL3.0 LISENCE
#商用利用する場合は、Ultralytics社と商用利用ライセンス契約をするか、全てのソールコードを一般公開して下さい。
#
#質問等の問い合わせ先
#メールアドレス daiya.seimitsu@gmail.com
#====================================================================


#モジュールの読み込み（変更不可）=======================================
import os #OSの処理に関するモジュールの読み込み
import sys #システムに関するモジュールの読み込み
import time #時間に関するモジュールの読み込み
import cv2 #画像処理モジュールの読み込み
from ultralytics import YOLO #AI物体検出モジュールの読み込み
#====================================================================


#変数設定1（変更不可）=================================================
cap = [] #cam_numで指定したカメラの台数分、VideoCaptureオブジェクトを格納するリスト
timer_start_time = 0 #設定した間隔で検出する為のタイマー用（開始の時間）
timer_current_time = 0 #設定した間隔で検出する為のタイマー用（開始の時間）
elapsed_time = 0 # #設定した間隔で検出する為のタイマー用（経過時間）
external_output = 0 #物体検出を外部機器に出力するか判定するフラグ（#####外部出力処理は未実装#####）
timer_process_start = 0 #検出処理時間計算用（開始時間）
timer_process_end = 0 #検出処理時間計算用（終了時間）
process_time = 0 #検出処理時間計算用（経過時間）
save_picture_num = 0 #写真を保存する際の現在の番号
save_dir_name = "picture" #写真を保存するディレクトリ名
save_picture_path = "" #検出した写真のパス
coco_names = [] #COCOデータセットの物体名を格納するクラス
file = "" #ファイルを読み込む為の変数
detected_name = "" #検出した物体の名前を格納
settings = [] #読み込んだ設定ファイルの各値を格納するリスト
detection_flag =0 #各カメラで対象物を検出したか確認するフラグ
#====================================================================


#設定ファイル内の各値を整形する関数=====================================
def value(setting): #関数を定義
    if "]" not in setting: #取得したデータに]文字があるか確認
        print("] character not found in a line of settings.") #エラーが発生した事を表示
        print("Exiting program.") #エラーが発生した事を表示
        sys.exit() #プログラムを強制終了
    setting = setting.split("]") #]文字で分割してリストに格納
    setting = setting[0].replace(" ", "") #スペース文字を削除
    setting = setting.replace("[", "") #[文字を削除
    print(setting) #整形した設定内容を表示
    return setting #整形した設定を返す
#====================================================================


#検出時にメールを送信する実装関連1（環境に合わせて設定を変更）============----------オリジナルに追加----------
#メールの接続テストは、「sample_settings_mail.txt」内を設定し（[]内に記述）、コマンドプロンプトで、例：python.exe c:/muma_miru/sample_send_mail.pyを実行して、「Sent mail successfully.」が表示されるか確認して下さい----------オリジナルに追加----------
print("Reading settings.") #設定ファイルを読み込んでいる事を表示----------オリジナルに追加----------
file = open("sample_settings_mail.txt", "r", encoding="utf-8") #sample_settings_mail.txtファイルの読み込み----------オリジナルに追加----------
settings = file.readlines() #ファイルの各行をリストに一括読み込み----------オリジナルに追加----------
file.close() #ファイルの読み込み終了----------オリジナルに追加----------
subject = value(settings[0]) #メールの件名----------オリジナルに追加----------
body_message = value(settings[1]) #メールの本文----------オリジナルに追加----------
sender_email_address = value(settings[2]) #送信元のメールアドレス----------オリジナルに追加----------
receiver_email_address = value(settings[3]) #送信先のメールアドレス----------オリジナルに追加----------
receivercc_email_address = value(settings[4]) #複数人にメールを送信する為のCC（メールアドレス間は,で区切る）----------オリジナルに追加----------
password = value(settings[5]) #smtpのパスワード（googleの場合はアプリパスワードを取得して設定して下さい https://myaccount.google.com/apppasswords ）----------オリジナルに追加----------
mail_server_address = value(settings[6]) #メールサーバーのアドレス（gmailの場合はsmtp.gmail.com）----------オリジナルに追加----------
mail_server_port = int(value(settings[7])) #メールサーバーのポート番号（gmailは465）----------オリジナルに追加----------
mail_ssl = int(value(settings[8])) #サーバーとのSSL通信する場合は1にする（通常のメールサーバーは殆どの場合0で、gmailのサーバーは1にする）----------オリジナルに追加----------
mail_interval = int(value(settings[9])) #メールする間隔を秒単位で指定（0はオフ）----------オリジナルに追加----------
#====================================================================----------オリジナルに追加----------


#検出時にメールを送信する実装関連2（変更不可）============----------オリジナルに追加----------
from sample_send_mail import send_mail #send_mail.pyファイルのsend_mail関数の読み込み----------オリジナルに追加----------
timer_mail_start = 0 #設定した間隔でメールを送信する為のタイマー用（開始の時間）----------オリジナルに追加----------
timer_mail_current = 0 #設定した間隔でメールを送信する為のタイマー用（現在の時間）----------オリジナルに追加----------
timer_mail_elapsed = 0  #設定した間隔でメールを送信する為のタイマー用（経過時間）----------オリジナルに追加----------
save_picture_path_list = "" #検出した写真のパスを格納するリスト----------オリジナルに追加----------
#====================================================================----------オリジナルに追加----------


#設定ファイルの読み込み================================================
print("Reading settings.") #設定ファイルを読み込んでいる事を表示
file = open("settings.txt", "r", encoding="utf-8") #設定ファイルの読み込み
settings = file.readlines() #ファイルの各行をリストに一括読み込み
file.close() #ファイルの読み込み終了
#====================================================================


#変数設定2（カメラ台数、適度な閾値、処理能力に合わせた設定に変更する）=====
cam_num = int(value(settings[0])) #PCに接続したカメラの台数を指定
det_conf = float(value(settings[1])) #検出の信頼度の閾値（小さくなる程誤検出が多くなり、大きくなる程検出しにくくなる）
cap_fps = float(value(settings[2])) #カメラのフレームレート（カメラから、毎秒何枚画像を取得するかを決める値）
timer_interval = float(value(settings[3])) #検出する間隔を秒単位で指定（0はオフ）（電気消費量を軽減します）
save_picture = int(value(settings[4])) #検出写真の保存有無
save_picture_num_MAX = int(value(settings[5])) #検出した写真の保存枚数
class_num = int(value(settings[6])) #21は熊の番号（cocoデータセット80種類内の一つ）（本プログラムのテストは、カメラを熊の画像に向けるか、値を0にして人を検出してください）
#====================================================================


#変数設定3（必要に応じて変更）==========================================
show_conf = 1 #検出した信頼度の表示有無
show_pic = 1 #画像表示有無
show_output = 1 #外部出力フラグの表示有無
show_process = 1 #検出処理時間の表示有無
#====================================================================


#変数設定4（通常は変更不要）===========================================
cap_x = 640 #カメラ解像度（横）
cap_y = 480 #カメラ解像度（縦）
#====================================================================


#変数設定5（下の学習済みモデルに行く程高性能だが、処理が重い）============
#学習済みモデル（５つの学習済みモデルのうち、使用する学習モデルのみ、先頭の#を削除）
#model_type = "yolo11n_ncnn_model/"
model_type = "yolo11s_ncnn_model/"
#model_type = "yolo11m_ncnn_model/"
#model_type = "yolo11l_ncnn_model/"
#model_type = "yolo11x_ncnn_model/"
weights = ["yolo11n", "yolo11s","yolo11m", "yolo11l", "yolo11x"] #変換する学習済みファイル名をリストに格納（拡張子なし）
#====================================================================


#オリジナルの学習済みモデルをncnn形式に変換==========================
for i in weights: #各変換前のファイル名をリストから取得
    if os.path.isfile(i + "_ncnn_model/metadata.yaml"): #指定したファイルがあるか確認
        print(i + " dataset for ncnn found.") #指定ファイルがある事を表示
    else: #指定したファイルが無かった場合
        if os.path.isfile(i + ".pt"): #指定したファイルがあるか確認
            model = YOLO(i + ".pt") #学習済みモデルの読み込み
            model.export(format="ncnn") #学習済みモデルの変換
            print("Converted " + i + ".pt to ncnn format.") #変換が成功した事を表示
        else: #指定したファイルが無い場合
            print(i +".pt was not found. Conversion is not excuted.") #ファイルが無かった事を表示
            model_name = model_type.split("_") #model_typeのモデル名のみを取得
            if model_name[0] == i: #変換不可の学習済みモデルが、指定した学習済みモデルと同じか確認
                print("Specified model " + model_name[0] + " does not exist. Program execution is forced to end.") #プログラムを強制終了する事を表示
                sys.exit() #指定した学習済みモデルが無い為、プログラムを強制終了 
#====================================================================


#学習済みモデルの読み込み==============================================
model = YOLO(model_type, task="detect")
#====================================================================


#カメラ指定した台数分設定==============================================
for i in range(cam_num): #cam_numで指定した回数、VideoCaptureオブジェクトを作成、設定する
    cap.append(cv2.VideoCapture(i)) #VideoCaptureオブジェクトを作成
    cap[i].set(3, cap_x) #カメラ解像度（横）を設定
    cap[i].set(4, cap_y) #カメラ解像度（縦）を設定
    cap[i].set(cv2.CAP_PROP_FPS, cap_fps) #カメラのフレームレートを設定
#====================================================================


#メインプログラム=====================================================
file = open("coco.names", "r") #coco.namesファイルの読み込み
coco_names = file.readlines() #ファイルの各行をリストに一括読み込み
file.close() #ファイルの読み込み終了
if os.path.exists(save_dir_name) ==False: #写真を保存するディレクトリが無いか確認
    os.mkdir(save_dir_name) #写真を保存するディレクトリを作成
while(True): #繰り返し処理
    if timer_mail_start == 0: #タイマーが開始していない場合----------オリジナルに追加----------
        timer_mail_start = time.time() #タイマーの開始時間を取得----------オリジナルに追加----------
    save_picture_path_list = [] #パスを初期化----------オリジナルに追加----------
    cv2.waitKey(1) #繰り返し処理では、ウィンドウの処理等がフリーズするので、割り込み処理を可能にする
    if timer_start_time == 0: #タイマーが開始していない場合
        timer_start_time = time.time() #タイマーの開始時間を取得
    timer_current_time = time.time() #現在の時間を取得
    elapsed_time = int(timer_current_time - timer_start_time) #経過時間を取得（整数に変換）
    if elapsed_time >= timer_interval: #経過時間が、設定した時間より大きいか確認
        timer_start_time = 0 #タイマーをリセット
        detected_sum = 0 #各カメラで検出した場合に1を加算し、全てのカメラ処理終了後に1以上なら、external_outputを1にする
        for i, j in enumerate(cap): #iはインデクス（0からの番号）、jは各VideoCaptureオブジェクト
            ret, frameA = j.read() #VideoCaptureオブジェクトで、カメラから画像を取得
            if ret: #カメラ画像取得に成功した場合
                detection_flag =0 #各カメラで対象物を検出したか確認するフラグをリセット
                timer_process_start = time.time() #検出処理時間計算用（開始時間）
                results = model.predict(source = frameA, classes = [class_num], imgsz = 640, conf = det_conf, device = "cpu", save = False,  project  = "", name = "", exist_ok = True)
                frameA = results[0].plot() #画像に検出結果をプロット
                for result in results: #検出結果の配列から、各検出結果を取得
                    boxes = result.boxes #バウンディングボックス等を格納した配列を取得、クラスID、信頼度を取得
                    for box in boxes: #バウンディングボックス等を格納した配列から各要素を取得
                        confident = int((float(box.conf) + 0.05) * 10) / 10 #検出した信頼度を取得
                        if show_conf == 1: #検出の信頼度を表示するか確認
                            print("CONFIDENT : " + str(confident)) #検出した信頼度を表示
                        detected_sum = detected_sum + 1 #検出したとして、1を加算
                        detection_flag = 1 #本カメラで物体を一つ以上検出したとする
                if save_picture == 1 and detection_flag == 1: #写真を保存するか 確認（物体を検出後）
                    save_picture_path = save_dir_name + "/" + str(save_picture_num) + ".jpg" #写真のパスを変数に格納
                    cv2.imwrite(save_picture_path, frameA) #写真番号をファイル名にして、写真を保存
                    save_picture_path_list.append(save_picture_path) #写真のパスを追加----------オリジナルに追加----------
                    save_picture_num = save_picture_num + 1 #次の写真番号にする
                    if save_picture_num == save_picture_num_MAX: #写真番号が上限に達したか確認
                        save_picture_num = 0 #写真番号をリセット
                if show_pic == 1: #画像を表示するか確認
                    cv2.imshow("CAMERA NUMBER : " + str(i), frameA) #画像を表示
                    timer_process_end = time.time() #検出処理時間計算用（終了時間）
                    process_time = int((timer_process_end - timer_process_start + 0.0005) * 1000) #検出処理時間計算用（終了時間）（ミリ秒で四捨五入）
                if show_process == 1: #処理時間を表示するか確認
                    print("PROCESS TIME : " + str(int(process_time)) + "ms") #検出時間を表示
                if show_pic == 1: #画像を表示するか確認
                    cv2.imshow("CAMERA NUMBER : " + str(i), frameA) #画像を表示
        if detected_sum > 0: #各カメラで検出したか確認
            external_output = 1 #外部機器に出力（オン）
        else: #検出していない場合
            external_output = 0 #外部機器に出力（オフ）
        if show_output == 1: #外部出力のフラグを表示するか確認
            if external_output == 1: #外部出力フラグが1の場合
                print("EXTERNAL OUTPUT : " + str(external_output)) #外部出力のフラグを表示
            else: #外部出力フラグが0の場合
                print("EXTERNAL OUTPUT : " + str(external_output)) #外部出力のフラグを表示
        if external_output == 1: #外部出力処理（#####外部出力処理は未実装#####）
            external_output = 0 #外部機器に出力（オフ）
            timer_mail_current = time.time() #現在の時間を取得----------オリジナルに追加----------
            timer_mail_elapsed = int(timer_mail_current - timer_mail_start) #経過時間を取得（整数に変換）----------オリジナルに追加----------
            if timer_mail_elapsed >= mail_interval: #経過時間が、設定した時間より大きいか確認----------オリジナルに追加----------
                timer_mail_start = 0 #タイマーをリセット----------オリジナルに追加----------
                send_mail(subject, body_message, sender_email_address, receiver_email_address, receivercc_email_address, password, mail_server_address, mail_server_port, save_picture_path_list, mail_ssl) #メールを送信する関数の実行（最後に検出した写真を送信）----------オリジナルに追加----------
    else: #経過時間が、設定した時間より小さい場合
        for i, j in enumerate(cap): #iはインデクス（0からの番号）、jは各VideoCaptureオブジェクト
            ret, frameA = j.read() #VideoCaptureオブジェクトで、カメラから画像を取得（映像のラグ発生防止の為、処理しない画像バッファを廃棄）
#====================================================================

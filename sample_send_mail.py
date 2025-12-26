#モジュールの読み込み==================================================
import os #OSの処理に関するモジュール
import smtplib #メール送信関連モジュール
from email.mime.multipart import MIMEMultipart #メール送信関連モジュール
from email.mime.text import MIMEText #メール送信関連モジュール
from email.mime.image import MIMEImage #メール送信関連モジュール
#====================================================================


def send_mail(subject, body_message, sender_email_address, receiver_email_address, receivercc_email_address, password, mail_server_address, mail_server_port, save_picture_path_list, mail_ssl): #関数を設定（送信元のメールアドレス, 送信先のメールアドレス, smtpのパスワード, 添付ファイルのパス）
    #メッセージの作成=====================================================
    msg = MIMEMultipart() #メッセージオブジェクトの作成
    msg['From'] = sender_email_address #送信元のメールアドレスを設定
    msg['To'] = receiver_email_address #送信先のメールアドレスを設定
    receiver_email_address = receiver_email_address.split(",") #テキストをリストに変換（server.sendmailの制限の為）
    if receivercc_email_address != "": #CCのメールアドレスが設定されているか確認
        msg['Cc'] = receivercc_email_address #CCのメールアドレスを設定
        receivercc_email_address = receivercc_email_address.split(",") #テキストをリストに変換（server.sendmailの制限の為）
    else: #CCのメールアドレスが設定されていない場合
        receivercc_email_address = [] #空のリストにする
    msg['Subject'] = subject #メールの件名を設定
    msg.attach(MIMEText(body_message, 'plain')) #メールの本文を設定
    for save_picture_path in save_picture_path_list: #写真の枚数分、添付ファイルを作成
        with open(save_picture_path, 'rb') as f: #ファイルのMIMEタイプを特定し、MIMEImageオブジェクトを作成
            picture_data = f.read() #データの読み込み
            picture = MIMEImage(picture_data) #写真を作成
            picture.add_header('Content-Disposition', 'attachment', filename=os.path.basename(save_picture_path)) #写真のファイル名を添付ファイル名として設定
            msg.attach(picture) #写真を添付
    #====================================================================


    #メールの送信処理=====================================================
    try: #エラーが発生しないか確認
        if mail_ssl == 0: #サーバーとの通信方式を確認（SSL通信でない場合）
            with smtplib.SMTP(mail_server_address, mail_server_port) as server: #SMTPサーバーに接続
                server.login(sender_email_address, password) #ログイン
                server.sendmail(sender_email_address, receiver_email_address + receivercc_email_address, msg.as_string()) #メールの送信
                server.quit() #接続解除
        else: #サーバーとの通信方式を確認（SSL通信の場合）
            with smtplib.SMTP_SSL(mail_server_address, mail_server_port) as server: #SMTPサーバーに接続
                server.login(sender_email_address, password) #ログイン
                server.sendmail(sender_email_address, receiver_email_address + receivercc_email_address, msg.as_string()) #メールの送信
                server.quit() #接続解除
        print("Sent mail successfully.") #メール送信成功を表示
    except Exception as e: #エラーが発生した場合
        print("Error occured while sending mail.") #メール送信失敗を表示
    #====================================================================


#本プログラムを直接起動してテストする為の処理============================
if __name__== "__main__": #本プログラムが直接起動された場合の処理
    import sys #システムに関するモジュールの読み込み
    def value(setting): #sample_settings_mail.txt内の各値を整形する関数
        if "]" not in setting: #取得したデータに]文字があるか確認
            print("] character not found in a line of sample_settings_mail.txt.") #エラーが発生した事を表示
            print("Exiting program.") #エラーが発生した事を表示
            sys.exit() #プログラムを強制終了
        setting = setting.split("]") #]文字で分割してリストに格納
        setting = setting[0].replace(" ", "") #スペース文字を削除
        setting = setting.replace("[", "") #[文字を削除
        print(setting) #整形した設定内容を表示
        return setting #整形した設定を返す
    file = open("sample_settings_mail.txt", "r", encoding="utf-8") #sample_settings_mail.txtファイルの読み込み
    mail_settings = file.readlines() #ファイルの各行をリストに一括読み込み
    file.close() #ファイルの読み込み終了
    subject = value(mail_settings[0]) #メールの件名
    body_message = value(mail_settings[1]) #メールの本文
    sender_email_address = value(mail_settings[2]) #送信元のメールアドレス
    receiver_email_address = value(mail_settings[3]) #送信先のメールアドレス
    receivercc_email_address = value(mail_settings[4]) #複数人にメールを送信する為のCC（メールアドレス間は,で区切る）
    password = value(mail_settings[5]) #smtpのパスワード（googleの場合はアプリパスワードを取得して設定して下さい https://myaccount.google.com/apppasswords ）
    mail_server_address = value(mail_settings[6]) #メールサーバーのアドレス（gmailの場合はsmtp.gmail.com）
    mail_server_port = int(value(mail_settings[7])) #メールサーバーのポート番号（gmailは465）
    mail_ssl = int(value(mail_settings[8])) #サーバーとのSSL通信する場合は1にする（通常のメールサーバーは殆どの場合0で、gmailのサーバーは1にする）
    mail_interval = int(value(mail_settings[9])) #メールする間隔を秒単位で指定（0はオフ）
    save_picture_path = "" #添付ファイル（画像）のパス
    send_mail(subject, body_message, sender_email_address, receiver_email_address, receivercc_email_address, password, mail_server_address, mail_server_port, save_picture_path, mail_ssl) #メールを送信する関数の実行
#====================================================================

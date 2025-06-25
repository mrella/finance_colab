#https://api.telegram.org/bot7823072621:AAHG2Id8hylX8RWoobQHDgPUCd_5Fj-BrRE/getChat?chat_id=@FinanceMR

import requests


BOT_TOKEN = "7823072621:AAHG2Id8hylX8RWoobQHDgPUCd_5Fj-BrRE"
CHAT_ID = "-1002887330790"
#CHAT_ID = "1659938216"

@staticmethod
def send(message):
        try:   
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": message,
                "disable_web_page_preview": "true"

            }
            response = requests.post(url, data=payload)

            print(f"Response Code: {response.status_code}")
            if response.ok:
                print("Message sent successfully")
            else:
                print("Error:", response.text)

        except Exception as e:
            print("Exception:", e)



def send_img(image_path, caption=""):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as image_file:
            files = {
                "photo": image_file
            }
            data = {
                "chat_id": CHAT_ID,
                    "caption": caption
              }
            response = requests.post(url, files=files, data=data)

        print(f"Response Code: {response.status_code}")
        if response.ok:
            print("Photo sent successfully")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Exception:", e)

def send_document(image_path, caption=""):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(image_path, "rb") as image_file:
            files = {
                "document": image_file
            }
            data = {
                "chat_id": CHAT_ID,
                    "caption": caption
              }
            response = requests.post(url, files=files, data=data)

        print(f"Response Code: {response.status_code}")
        if response.ok:
            print("Photo sent successfully")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Exception:", e)



def send_video(video_path, caption=""):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
        with open(video_path, "rb") as video_file:
            files = {
                "video": video_file
            }
            data = {
                "chat_id": CHAT_ID,
                "caption": caption
            }
            response = requests.post(url, files=files, data=data)

        print(f"Response Code: {response.status_code}")
        if response.ok:
            print("Video sent successfully")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Exception:", e)




import requests, os

bot_token = 'xxx:xxx'
stickerName = 'GenshinLolis'


StickerSet = requests.get(f"https://api.telegram.org/bot{bot_token}/getStickerSet", data={'name':stickerName}).json()

def downloadByFileId(fileId):
    File = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile", data={'file_id':fileId}).json()
    path = File['result']['file_path']
    fileName = path.split('/')[-1]
    StickerContent = requests.get(f"https://api.telegram.org/file/bot{bot_token}/{path}").content
    
    if not os.path.exists(f"./{StickerSet['result']['name']}"):
        os.mkdir(f"./{StickerSet['result']['name']}")
    with open(f"./{StickerSet['result']['name']}/{fileName}","wb") as f:
        f.write(StickerContent)
    print(f'{fileName} 下载成功')
    
import threading

taskList = []

for i in StickerSet['result']['stickers']:
    taskList.append(
        threading.Thread(target=downloadByFileId,args=(i['file_id'],))
    )

for th in taskList:
    th.start()
    
for th in taskList:
    th.join(10)

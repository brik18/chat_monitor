
import os
import pandas as pd
import time
from pytchat import LiveChat, CompatibleProcessor
import pytchat
import sys
print(sys.path)
# tiempo inicio, tiempo actual
start_time = time.time()
print(os.environ.get('PYTHONPATH'))
data = []


def save_chat(nombre_archivo, df):  # escritura de archivos en python
    with open(nombre_archivo, 'w') as archivo:
        # archivo.write(df)
        archivo.write(df.to_csv(index=False))
    return "Archivo guardado exitosamente"


def monitor(url: str):
    chat = pytchat.create(video_id=url)
    while chat.is_alive():
        if time.time() - start_time > 60:  # 600 segundos son 10 minutos
            save_chat('D:\\areas\\universidad\\proyecto_de_grado\\api_chats_live\\mi_archivo.txt',
                      df)
            break
        for c in chat.get().sync_items():
            #df = (f"{c.datetime}|{c.message}|{c.type}|{c.messageEx}|{c.author.name}|{c.author.channelId}|{c.author.channelUrl}|{c.author.imageUrl}|{c.author.isChatOwner}|{c.author.isChatSponsor}|{c.author.isChatModerator}|{c.author.isVerified}")
            nueva_linea_time = (f"{c.datetime}")
            nueva_linea_message = (f"{c.message}")
            #df = (f"{c.datetime}|{c.message}")
            nueva_fila = {'time': nueva_linea_time,
                          'message': nueva_linea_message}
            data.append(nueva_fila)
            df = pd.DataFrame(data)
            print(f"{c.datetime}|{c.message}")


# if __name__ == "__main__":
#    monitor(url=args.url)
monitor("https://www.youtube.com/watch?v=C_dXWOO9fwo")

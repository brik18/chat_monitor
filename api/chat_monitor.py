import argparse
import datetime
import os
import pytchat
import sys
import csv


# tiempo inicio, tiempo actual
start_time = datetime.datetime.now()


def save_chat(f_data, data):  # escritura de archivos en python
    writter = csv.writer(f_data, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    writter.writerow(data)
    f_data.flush()


def monitor(url: str):
    try:
        chat = pytchat.create(video_id=url)
        f_data = open_f_data()
        save_chat(f_data, ["time", "message"])
        n_files = 1
        rotate_seconds = 180
        while chat.is_alive():
            for c in chat.get().sync_items():
                # df = (f"{c.datetime}|{c.message}|{c.type}|{c.messageEx}|{c.author.name}|{c.author.channelId}|{c.author.channelUrl}|{c.author.imageUrl}|{c.author.isChatOwner}|{c.author.isChatSponsor}|{c.author.isChatModerator}|{c.author.isVerified}")
                message = [c.datetime, c.message]
                save_chat(f_data, message)
                print(f"{c.datetime}|{c.message}")
            # if the current time is 15 minutes after the start time
            if (
                datetime.datetime.now() - start_time
            ).seconds > rotate_seconds * n_files:
                # close the file
                close_f_data(f_data)
                # open a new file
                f_data = open_f_data()
                # increment the file counter
                n_files += 1

        close_f_data(f_data)
    except Exception as e:
        print(e)
        close_f_data(f_data)
        sys.exit(1)


def open_f_data():
    # get the current date and time
    now = datetime.datetime.now()
    # get the current date and time in a string format
    current_time = now.strftime("%y%m%d_%H%M%S")
    # open the file with the current date and time
    f_data = open(f"data/{current_time}.csv", "w", encoding="UTF-8")
    # return the file reference
    return f_data


def close_f_data(f_data):
    # close the file
    if f_data is not None and not f_data.closed:
        f_data.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("ChatMonitor")
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    monitor(url=args.url)

# monitor("https://www.youtube.com/watch?v=C_dXWOO9fwo")

import subprocess
import psutil
import os
import datetime
import pandas as pd
from time import sleep


def start_monitoring(url: str):
    try:
        stop_monitoring()
        p = subprocess.Popen(["python", "chat_monitor.py", f"--url={url}"])
        __save_pid(p.pid)
        return {"pid": p.pid}
    except Exception as e:
        return {
            "error": str(e),
            "message": f"unable to start monitoring for the url:{url}",
        }


def stop_monitoring():
    try:
        pid = __get_pid()
        response = {"pid": pid, "status": "stoped"}
        if pid is None:
            __clean_data()
            __clean_pid()
            return {"pid": pid, "status": "monitoring process is not running"}
        process = psutil.Process(pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except psutil.NoSuchProcess:
        response = {"pid": pid, "status": "not found"}
    sleep(1)
    __clean_data()
    __clean_pid()
    return response


def analize_chat():
    try:
        data = __get_data()
        df = pd.concat(data)
        df["time"] = pd.to_datetime(df["time"])
        df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df = df.sort_values(by=["time"])
        df = df.reset_index(drop=True)
        if not os.path.exists("analized"):
            os.mkdir("analized")
        current = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        df.to_csv(f"analized/analized_{current}.csv", index=False)
    except Exception as e:
        return {"error": str(e), "message": "unable to analize chat"}
    return df


# read all csv files in data folder and return a list of dataframes
def __get_data():
    data = []
    for file in os.listdir("data"):
        if file.endswith(".csv"):
            data.append(pd.read_csv(f"data/{file}"))
    return data


def __clean_data():
    if os.path.exists("data"):
        os.rename(
            "data", f"data_old_{datetime.datetime.now().strftime('%y%m%d_%H%M%S')}"
        )
    os.mkdir("data")


def __clean_pid():
    if os.path.exists("pid.txt"):
        os.remove("pid.txt")


def __save_pid(pid: int):
    with open("pid.txt", "w") as f:
        f.write(str(pid))


def __get_pid() -> int:
    pid = None
    if os.path.exists("pid.txt"):
        with open("pid.txt", "r") as f:
            pid = int(f.read())
    return pid

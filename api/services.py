import subprocess
import sys
import psutil
import os
import datetime
import pandas as pd
from time import sleep
from pysentimiento import create_analyzer
import logging
import traceback

logging.basicConfig(level=logging.INFO)


base_file_path = os.path.dirname(os.path.abspath(__file__))

def start_monitoring(url: str):
    try:
        stop_monitoring()
        chat_monitor_file = os.path.join(base_file_path, "chat_monitor.py")
        python_sys_path = sys.executable
        p = subprocess.Popen([python_sys_path, chat_monitor_file , f"--url={url}"])
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
        analized_dir = os.path.join(base_file_path, "analized")
        if not os.path.exists(analized_dir):
            os.mkdir(analized_dir)
        current = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        analized_file = os.path.join(base_file_path, "analized", f"analized_{current}.csv")
        analized_results = os.path.join(base_file_path,"analized" , f"analized_{current}_results.txt")
        df.to_csv(analized_file, index=False)
        chats = df["message"].tolist()
        results = __predict_sentimens(chats)
        __save_results(analized_results, results)
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e) , "message": "unable to analize chat"}
    return {"results": results, "time": current}


def __save_results(analized_results, data):  # escritura de archivos en python
    with open(analized_results, "w+") as f_data:
        f_data.write(str(data))


def __predict_sentimens(chats):
    analyzer = create_analyzer(task="sentiment", lang="es")
    results = analyzer.predict(chats)
    prediction = [ {"output": x.output, "val": 1 } for x in results ]
    df = pd.DataFrame.from_dict(prediction)
    df = df.groupby(["output"])["output"].count()
    _data = df[:]/len(chats)
    return {
            "NEG": _data["NEG"] if "NEG" in _data.keys() else 0,
            "NEU": _data["NEU"] if "NEU" in _data.keys() else 0,
            "POS": _data["POS"] if "POS" in _data.keys() else 0
            }

# read all csv files in data folder and return a list of dataframes
def __get_data():
    data = []
    data_dir_name = os.path.join(base_file_path, "data")
    for file in os.listdir(data_dir_name):
        if file.endswith(".csv"):
            data.append(pd.read_csv(f"{data_dir_name}/{file}"))
    return data


def __clean_data():
    data_dir_name = os.path.join(base_file_path, "data")
    old_data_dir_name = os.path.join(base_file_path, f"data_old_{datetime.datetime.now().strftime('%y%m%d_%H%M%S')}")
    if os.path.exists(data_dir_name):
        os.rename(
            data_dir_name, old_data_dir_name
        )

    os.mkdir(data_dir_name)


def __clean_pid():
    pid_file_path = os.path.join(base_file_path, "pid.txt")
    if os.path.exists(pid_file_path):
        os.remove(pid_file_path)


def __save_pid(pid: int):
    pid_file_path = os.path.join(base_file_path, "pid.txt")
    with open(pid_file_path, "w") as f:
        f.write(str(pid))


def __get_pid() -> int:
    pid_file_path = os.path.join(base_file_path, "pid.txt")
    pid = None
    if os.path.exists(pid_file_path):
        with open(pid_file_path, "r") as f:
            pid = int(f.read())
    return pid

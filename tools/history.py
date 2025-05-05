import datetime
import os

import pandas as pd

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "session_logs.csv")
def log_session_event(event):
    log_path = "../session_logs.csv"
    df = pd.DataFrame([{
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event
    }])
    df.to_csv(log_path, mode='a', header=not os.path.exists(log_path), index=False)


def history():

 history()
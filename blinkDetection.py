
from collections import deque
import pandas as pd
import numpy as np
import os

CSV_FILENAME = "blink_training_data.csv"



class DataCollection:
    def __init__(self,session_lable):
        self.blink_timestamps = []
        self.data_rows = []
        self.lable = session_lable
        self.closed_eye = False
      
        
    def addTimestamp(self,timestamp,):
        self.blink_timestamps.append(timestamp)
    def blinkCount(self):
        return len(self.blink_timestamps)
    def otherData(self):
        if self.blinkCount() > 1:
        # Calculate seconds between consecutive timestamps
            intervals = np.diff(list(self.blink_timestamps))
            mean_ibi = np.mean(intervals)
            std_ibi = np.std(intervals)
        else:
            mean_ibi = 60.0 
            std_ibi = 0.0
        return {"mean":mean_ibi,"std":std_ibi}
    def store_data(self):
        if not os.path.exists(CSV_FILENAME):
            df = pd.DataFrame(columns=["blink_count", "mean_ibi", "ibi_std", "target"])
            df.to_csv(CSV_FILENAME, index=False)
        data = self.otherData()
        row = {
            "blink_count": self.blinkCount(),
            "mean_ibi": data["mean"],
            "ibi_std": data["std"],
            "target": self.lable,
        }
        final_data = pd.DataFrame([row])
        final_data.to_csv(CSV_FILENAME, mode='a', header=False, index=False)
        self.blink_timestamps=[]
        print("stored")
        
    
    
    
    
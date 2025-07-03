import logging
import datetime
import os

logs_dir = os.path.join(os.getcwd(),"logs")  # Creates a path like C:\Users\kunsh\Test GIT\logs
os.makedirs(logs_dir, exist_ok=True) # Creates folder and exist_ok =True means no error if already exists
log_filename = f"{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_file_path = os.path.join(logs_dir,log_filename)  # C:\Users\kunsh\project\logs\07_03_2025_15_21_52.log

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
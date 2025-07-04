import sys # Helps in reacting when an exception is raised
import traceback # Helps in getting info of the exception raised
from src.logger import logging #Extrats the logging info we need to save in the folder LOGS


class CustomException(Exception): # Build in Exception class is used and CustomException is the chlid class
    def __init__(self,error):
        trace = traceback.extract_tb(sys.exc_info()[2])
        for log in trace:
            logging.error(f"For the file {log.filename} , in the line {log.lineno} , the error is {error}")
        # exc_info --> Helps in getting the tuple with error,line no and Traceback ( Therefore [2])
        filename = log.filename
        lineno = log.lineno
        self.message = f"Error occured in the script {filename} , line {lineno} , message : {str(error)}"

        logging.error(self.message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


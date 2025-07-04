import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransferConfig

@dataclass # This decorator helps in bypassing the __init__ inside the class to define any variable
class DataIngestionConfig: # Creation of the paths for the data present
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    raw_data_path = os.path.join("artifacts","raw.csv")

class DataIngestion:
    def __init__(self): # helps in getting the access to that train ,test and raw data file paths
        self.ingestion_config = DataIngestionConfig()

    def initate_data_ingestion(self):  # creates train , test and raw data into the file pats mentioned
        logging.info("Data Entery Method Has Been Started")
        try:
            df = pd.read_csv("data.csv")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info('Train Test Started')

            train_set,test_set = train_test_split(df,test_size=0.20)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion Of Data Has Been Completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion() 
    train_path,test_path=obj.initate_data_ingestion()
    data_transformation = DataTransformation()
    data_transformation.transform_data(train_path,test_path)
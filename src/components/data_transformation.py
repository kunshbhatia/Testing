### Done Data Transformation including creating pipelines,column transformation , fit_transform the
#   data and saving the model.

import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.utlis import save_object

@dataclass
class DataTransferConfig:
    preprocessor_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transfer_config = DataTransferConfig()

    def build_preprocessor(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                
                steps=[
                    ("imputer",SimpleImputer(strategy="median")), #Working as fillna()
                    ("scaler",StandardScaler())

                ])

            cat_pipeline = Pipeline(
                
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ('encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ])
            
            logging.info(f"Catrgorical Features : {categorical_columns}")
            logging.info(f"Numerical Features : {numerical_columns}")
            
            preprocessing = ColumnTransformer(
                [
                    ("Cat_features",cat_pipeline,categorical_columns),
                    ("Num_features",num_pipeline,numerical_columns)
                ]
            )

            return preprocessing  
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def transform_data(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Train and test data loaded.")

            target = "math_score"
            X_train = train_df.drop(columns=[target])
            y_train = train_df[target]
            X_test = test_df.drop(columns=[target])
            y_test = test_df[target]

            preprocessor = self.build_preprocessor()
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            save_object( # IN utils , helps in saving pickle file
                filepath=self.data_transfer_config.preprocessor_path,
                obj=preprocessor
            )

            logging.info("Object Saved To File Path")

            train_data_array = np.c_[X_train_transformed,pd.Series(y_train)]
            test_data_array = np.c_[X_test_transformed,pd.Series(y_test)]

            processor_path = self.data_transfer_config.preprocessor_path
            
            return (
                train_data_array,
                test_data_array,
                processor_path
            )
        except Exception as e:
            raise CustomException(e)
        




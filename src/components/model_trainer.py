import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utlis import save_object,evaluate_model

#from src.utlis import save_object,evaluate_models

class ModelTrainerConfig:
    trained_model_config = os.path.join("artifacts","model.pkl")

class ModelTraining:
    def __init__(self):
        self.model_train_config = ModelTrainerConfig()

    def initiate_model_training(self,train_data_array,test_data_array):
        try:
            logging.info("Splitting Train and Test input data")
            X_train,Y_train,X_test,Y_test = (
                train_data_array[:,:-1],
                train_data_array[:,-1],
                test_data_array[:,:-1],
                test_data_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }

            model_report = evaluate_model(X_train=X_train,Y_train=Y_train,X_test=X_test,Y_test=Y_test,models=models,params=params)

            best_model_score = max(sorted(model_report.values()))
            best_model = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            logging.info("Best model Found")

            save_object(
                filepath=self.model_train_config.trained_model_config,
                obj= best_model
            )

            logging.info(f"Best Model is {best_model} having a score of {best_model_score*100}")

        except Exception as e:
            raise CustomException(e)
import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(filepath,obj):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e,sys)

def evaluate_model(X_train,X_test,Y_train,Y_test,models,params):

    report = {}
    for i in range(len(list(models))):
        model = list(models.values())[i]
    
    preprocessing = [
        (model_name, models[model_name], params[model_name])
        for model_name in models
    ]

    for name,mod,param in preprocessing:
        gs = GridSearchCV(estimator=mod,param_grid=param,n_jobs=-1,cv=3)
        gs.fit(X_train,Y_train)
        best_model = gs.best_estimator_

        Y_test_predict = best_model.predict(X_test)

        test_score = r2_score(Y_test,Y_test_predict)

        report[list(models.keys())[i]] = test_score

    return report

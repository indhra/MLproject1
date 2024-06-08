import pandas as pd 
import numpy as np

import sys 
import os

from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object 


@dataclass
class DataTransformationConfig:
    pre_processor_obj_file = os.path.join('artifacts','preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        """ 
        this function is responsible for data transformation
        
        """
        try:
            numerical_columns = ['writing score','reading score']
            categorical_columns = [
                'gender', 
                'race/ethnicity', 
                'parental level of education',
                'lunch',
                'test preparation course'
            ]
            
            
            logging.info(f'categorical columns {categorical_columns} ')
            logging.info(f'Numerical columns {numerical_columns}')
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('oneHotEncoder',OneHotEncoder()),
                    ('scaling',StandardScaler(with_mean=False))
                ]
            )
            
            logging.info('categorical columns encoding completed')
            logging.info('Numerical columns standard scaling completed')
            
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)
                    
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def inititate_data_transofrmation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)        
            test_df=pd.read_csv(test_path)
            
            logging.info('the train and test read completed')
            logging.info('obtaining preprocessing object')
            
            preprocessing_obj = self.get_data_transformer_object()
            
            
            target_column = 'math score'
            numerical_cols = ['writing score','reading score']
            
            input_feature_train_df=train_df.drop(columns=[target_column], axis =1 )
            target_feat_train_df=train_df[target_column]
            
            input_feat_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feat_test_df = test_df[target_column]
            
            logging.info(
                'applying preproceessing object on training dataframe and testing datagrame.'
            )
            
            input_feat_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feat_test_df)
            
            train_arr=np.c_[
                input_feat_train_arr,np.array(target_feat_train_df)
            ]
            
            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feat_test_df)
            ]
            
            logging.info('saved preprocessing object.')
            
            save_object(
                file_path=self.data_transformation_config.pre_processor_obj_file,
                objt=preprocessing_obj
                
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.pre_processor_obj_file
            )
        except Exception as e:
            1
            raise CustomException(e,sys)
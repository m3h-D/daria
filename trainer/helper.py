
# وارد کردن کتابخانه‌های مورد نیاز
import os
import numpy as np 
import yaml
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from xgboost import XGBClassifier
from django.conf import settings
from trainer import exceptions



#* this code can be modulated, just because the training models are limited and the logic is specific, modulating is over work.




class DataLoader:
    def __init__(self, config):
        self.config = config

    def missing_data(self, data):
        return data.isnull().sum()

    def load(self, data_cross, data_long):
        # main_path = os.path.join(os.getcwd(), "data")

        # # بارگذاری داده‌های cross-sectional
        # data_cross = pd.read_csv(os.path.join(main_path,'cross.csv'))

        # # بارگذاری داده‌های longitudinal
        # data_long = pd.read_csv(os.path.join(main_path,'long.csv'))
        data = pd.concat([data_cross, data_long])
        data.head()
        for column in data.columns:
            mode_value = data[column].mode()
            data[column].fillna(mode_value[0], inplace=True)
        return data

class PreprocessorBuilder:
    @staticmethod
    def build(scale_cols, ohe_cols):
        return ColumnTransformer([
            ('scale', StandardScaler(), scale_cols),
            ('ohe', OneHotEncoder(), ohe_cols)
        ])

class ClassifierModelFactory:
    MODELS = {
        'xgboost': XGBClassifier,
        'random_forest': RandomForestClassifier
    }

    @classmethod
    def get(cls, model_type, kwargs=None):
        kwargs = kwargs or {}
        try:
            return cls.MODELS[model_type](**kwargs)
        except KeyError:
            raise exceptions.ModelTypeNotValidException(f"{model_type} is not supported")



class Trainer:
    def __init__(self, preprocessor, classifier):
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', classifier)
        ])
        self.label = LabelEncoder()

    def train(self, y_train, y_val, X_train):
        #? not sure if creating self property in this method is OK
        self.y_train_label = self.label.fit_transform(y_train)
        self.y_test_label = self.label.transform(y_val)
        self.pipeline.fit(X_train, self.y_train_label)
        return self

    def score(self, X_val):
        return self.pipeline.score(X_val, self.y_test_label)

    def get_classification_report(self, X_val):
        return classification_report(self.y_test_label, self.pipeline.predict(X_val), output_dict=True)

    def predict_proba(self, X_val):
        return self.pipeline.predict_proba(X_val)

class TrainHandler:
    def __init__(self, data_cross, data_long, config_path=None):
        config_path = config_path or os.path.join(settings.BASE_DIR, 'trainer/config.yml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.data_loader = DataLoader(self.config)
        self.data = self.data_loader.load(data_cross, data_long)

        self.X_train, self.X_val, self.y_train, self.y_val = self._split_data()
        self.preprocessor = PreprocessorBuilder.build(
            self.config['features']['scale'],
            self.config['features']['ohe']
        )

    def _split_data(self):
        X = self.data.drop(self.config['features']['drop_columns'], axis=1)
        y = self.data[self.config['features']['label']]
        X_train, X_val, y_train, y_val = train_test_split(X, y, **self.config['split'])
        return X_train, X_val, y_train, y_val

    def _get_classifier(self, model_name):
        kwargs = self.config['classifier'].get(model_name, {})
        return ClassifierModelFactory.get(model_name, kwargs)

    def train(self, model_name='random_forest'):
        classifier = self._get_classifier(model_name)
        self.trainer = Trainer(self.preprocessor, classifier).train(self.y_train, self.y_val, self.X_train)

    def get_rf_result(self):
        if not hasattr(self, 'trainer'):
            raise exceptions.TrainModelException("Model not trained yet.")
        return self.trainer.get_classification_report(self.X_val)

    def get_prob_y(self):
        if not hasattr(self, 'trainer'):
            raise exceptions.TrainModelException("Model not trained yet.")
        return self.trainer.predict_proba(self.X_val)

    def accuracy(self):
        if not hasattr(self, 'trainer'):
            raise exceptions.TrainModelException("Model not trained yet.")
        return self.trainer.score(self.X_val)

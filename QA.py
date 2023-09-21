import joblib
import pandas as pd
from ast import literal_eval

from cdqa.utils.filters import filter_paragraphs
from cdqa.utils.download import download_model, download_bnpp_data
from cdqa.pipeline.cdqa_sklearn import QAPipeline

# Download data and models
#download_model(model='bert-squad_1.1', dir='./models')

# Loading data and filtering / preprocessing the documents
df = pd.read_csv('data/trainQuestions.csv', converters={'paragraphs': literal_eval})
df = filter_paragraphs(df)
cdqa_pipeline = QAPipeline(reader='./models/bert_qa.joblib')

# Fitting the retriever to the list of documents in the dataframe
cdqa_pipeline.fit_retriever(df=df)

joblib.dump(cdqa_pipeline, './models/bert_wells_qa.joblib')

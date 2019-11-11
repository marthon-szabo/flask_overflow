import csv
import os
import server.py
import connection.py

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv', 'sample_data/question.csv'

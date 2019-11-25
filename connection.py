import os
import psycopg2
import psycopg2.extras

def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name
        # this string describes all info for psycopg2 to connect to the database
    if env_variables_defined:
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError("Something wrong")



def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()


"""
import csv
import datetime

answers = []
question_head = ['id','submission_time','view_number','vote_number','title','message','image']
questions = []
answer_head = ['id', 'submission_time','vote_number','question_id','message','image']


def sort_dict_by_key(table, key_, isint):
    if isint:
        return sorted(table, key=lambda k: int(k[key_]))
    else:
        return sorted(table, key=lambda k: k[key_].lower())
def read_answers():
    with open('sample_data/answer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            answers.append(record)

def write_answers():
    with open('sample_data/answer.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=answer_head)
        writer.writeheader()
        for record in answers:
            writer.writerow(record)

def read_questions():
    with open('sample_data/question.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            questions.append(record)

def write_questions():
    with open('sample_data/question.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=question_head)
        writer.writeheader()
        for record in questions:
            writer.writerow(record)

def add_question(title,message,image):
    question = {
        'id':str(int(get_max_question_id())+1),
        'submission_time':str(datetime.datetime.now())[:16],
        'view_number':'0',
        'vote_number':'0',
        'title':title,
        'message':message,
        'image':image
    }
    questions.append(question)
    write_questions()

def add_answer(message, image,question_id):
    record = {
        'id':str(int(get_max_anws_id(question_id)) + 1),
        'submission_time':str(datetime.datetime.now())[:16],
        'question_id' : str(question_id),
        'vote_number':'0',
        'message':message,
        'image':image
    }
    answers.append(record)
    write_answers()

def get_max_anws_id(question_id):
    id = 0
    for record in answers:
        id = record['id']
    return id

def get_max_question_id():
    id = 0
    for record in questions:
        id = record['id']
    return id

def like_post(id_):
    for record in answers:
        if int(record['id']) == int(id_):
            record['vote_number'] = str(int(record['vote_number']) + 1)
    write_answers()

def dislike_post(id_):
    for record in answers:
        if int(record['id']) == int(id_):
            record['vote_number'] = str(int(record['vote_number']) - 1)
    write_answers()

def get_max_voted(question_id):
    if len(answers)>0:
        max_like = None
    else:
        return 0
    for record in answers:
        if int(question_id) == int(record['question_id']):
            if not max_like:
                max_like = int(record['vote_number'])
            else:
                if int(record['vote_number']) > max_like:
                    max_like = int(record['vote_number'])
    return max_like

def like_question(id_):
    for record in questions:
        if int(record['id']) == int(id_):
            record['vote_number'] = str(int(record['vote_number']) + 1)
    write_questions()

def dislike_question(id_):
    for record in questions:
        if int(record['id']) == int(id_):
            record['vote_number'] = str(int(record['vote_number']) - 1)
    write_questions()

def view_question(id_):
    for record in questions:
        if int(record['id']) == int(id_):
            record['view_number'] = str(int(record['view_number']) + 1)
    write_questions()

def delete_anwser(id_):
    global answers
    new_table = []
    for record in answers:
        if int(record['id']) != int(id_):
            new_table.append(record)
    answers = new_table
    write_answers()

def delete_question(id_):
    global questions
    global answers
    new_table = []
    for record in questions:
        if int(record['id']) != int(id_):
            new_table.append(record)
    questions = new_table
    new_table = []
    for record in answers:
        if int(record['question_id']) != int(id_):
            new_table.append(record)
    answers = new_table
    write_answers()
    write_questions()

def search_table(searchtag):
    new_table=[]
    global questions
    if searchtag.replace(' ','') == '':
        return questions
    else:
        for record in questions:
            if record['title'].lower().find(searchtag) >= 0:
                new_table.append(record)
        return new_table

def edit_question(id_, title, message, image):
    global questions
    for question in questions:
        if int(question['id']) == int(id_):
            question['message'] = message
            question['title'] = title
            question['image'] = image
    write_questions()
"""
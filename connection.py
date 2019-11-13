import csv
import datetime

answers = []
question_head = ['id','submission_time','view_number','vote_number','title','message','image']
questions = []
answer_head = ['id', 'submission_time','vote_number','question_id','message','image']

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
        'submission_time':str(datetime.datetime.now()),
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
        'submission_time':str(datetime.datetime.now()),
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
    max_like = 0
    for record in answers:
        if int(question_id) == int(record['question_id']):
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
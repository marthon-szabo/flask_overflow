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
        'id':get_max_question_id(),
        'submission_time':str(datetime.datetime.now()),
        'view_number':'0',
        'vote_number':'0',
        'title':title,
        'message':message,
        'image':image
    }
    questions.append(question)
    write_questions()

def get_max_question_id():
    id = 0
    for record in questions:
        id = record['id']
    return id

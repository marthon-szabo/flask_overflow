import connection
from datetime import datetime

def get_timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return timestamp

def get_time():
    return datetime.today()

def numbert_to_timestamp(submission_time):
    return datetime.datetime.fromtimestamp(submission_time / 1e3)

@connection.connection_handler
def get_question(cursor,id_):
    cursor.execute("""
    SELECT * FROM question
    WHERE id = %(id)s;
    """,{'id':id_})
    return cursor.fetchall()

@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
    SELECT * FROM question
    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_answers(cursor,question_id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE  question_id = %(id)s
    ORDER BY vote_number ASC;
    """,{'id':question_id})
    return cursor.fetchall()

@connection.connection_handler
def add_question(cursor,title,message,image,submission_time):
    cursor.execute("""
        INSERT INTO question
        (title, message, image, submission_time, view_number, vote_number)
        VALUES (%(title)s,%(message)s,%(image)s,%(submission_time)s,0,0)
    """,{'title':title, 'message':message, 'image':image, 'submission_time':submission_time}
    )

@connection.connection_handler
def add_answer(cursor,message, image,question_id,submission_time):
    #submission_time = timestamp_to_number(submission_time)
    cursor.execute("""
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s);
    """,{'submission_time':submission_time,'question_id':question_id, 'message':message,'image':image})

@connection.connection_handler
def like_post(cursor,id_): #like answer
    cursor.execute("""
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;
    """,{'id':id_})

@connection.connection_handler
def dislike_post(cursor,id_): #dislike answer
    cursor.execute("""
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(id)s
    """, {'id':id_})


@connection.connection_handler
def like_question(cursor,id_):
    cursor.execute("""
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;
    """, {'id':id_})

@connection.connection_handler
def dislike_question(cursor, id_):
    cursor.execute("""
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(id)s;
    """, {'id':id_})

@connection.connection_handler
def view_question(cursor, id_):
    cursor.execute("""
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(id)s;
    """, {'id':id_})

@connection.connection_handler
def delete_anwser(cursor,id_):
    cursor.execute("""
    DELETE FROM answer
    WHERE id = %(id)s;
    """, {'id': id_})

@connection.connection_handler
def delete_question(cursor, id_):

    cursor.execute("""ALTER TABLE question DISABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE comment DISABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE answer DISABLE TRIGGER ALL;""")

    cursor.execute("""
    DELETE FROM question
    WHERE id = %(id)s;
    """,{'id':id_})


    cursor.execute("""
    DELETE FROM comment
    WHERE question_id = %(cid)s
    """, {'cid':id_})

    cursor.execute("""
        DELETE FROM answer
        WHERE question_id = %(id)s
    """, {'id':id_})

    cursor.execute("""ALTER TABLE answer ENABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE comment ENABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE question ENABLE TRIGGER ALL;""")





@connection.connection_handler
def search_table(cursor, searchtag):
    cursor.execute("""
        SELECT * FROM question
        WHERE title ILIKE %(search)s;
    """, {'search':searchtag})
    return cursor.fetchall()

@connection.connection_handler
def edit_question(cursor, id_, title, message, image):
    cursor.execute("""
    UPDATE question 
    SET title = %(title)s, message = %(message)s, image = %(image)s
    WHERE id = %(id)s;
    """,{'title':title, 'message':message, 'image':image, 'id':id_}
    )


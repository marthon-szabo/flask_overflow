from psycopg2 import sql
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
    return cursor.fetchone()

@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
    SELECT * FROM question;
    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_latest_questions(cursor):
    cursor.execute("""
    SELECT * FROM question
    ORDER BY submission_time DESC
    LIMIT 5;
    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def sort_question_by(cursor, sort_by, direction):
    if direction == 'ASC':
        cursor.execute(sql.SQL("""
        SELECT * FROM question
        ORDER BY {} ASC
         """).format(sql.Identifier(sort_by)))
    else:
        cursor.execute(sql.SQL("""
        SELECT * FROM question
        ORDER BY {} DESC
         """).format(sql.Identifier(sort_by)))


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
def add_question(cursor,title,message,image):
    submission_time = get_time()
    cursor.execute("""
        INSERT INTO question
        (title, message, image, submission_time, view_number, vote_number)
        VALUES (%(title)s,%(message)s,%(image)s,%(submission_time)s,0,0)
    """,{'title':title, 'message':message, 'image':image, 'submission_time':submission_time}
    )

@connection.connection_handler
def get_subcomments(cursor):
    cursor.execute("""
        SELECT * FROM comment
    """)
    return cursor.fetchall()

@connection.connection_handler
def get_question_subcomments(cursor,question_id):
    cursor.execute("""
        SELECT * FROM comment
        WHERE NOT (question_id IS NULL)
        AND question_id = %(id)s
    """, {'id':question_id})
    return cursor.fetchall()

@connection.connection_handler
def add_subbcomment_to_question(cursor, question_id, message):
    cursor.execute("""
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(question_id)s, NULL, %(message)s, %(timenow)s, 0 )
    """, {'question_id':question_id, 'message':message, 'timenow':get_time()})

@connection.connection_handler
def get_max_like(cursor,question_id):
    cursor.execute("""
        SELECT MAX(vote_number) FROM answer
        WHERE question_id = %(id)s
    """,{'id':question_id})
    number = cursor.fetchone()
    return number['max']

@connection.connection_handler
def add_subbcomment_to_answer(cursor, answer_id, message):
    cursor.execute("""
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
    VALUES (NULL, %(id_)s, %(msg)s, %(timenow)s, 0)
    """, {'id_':answer_id, 'msg':message, 'timenow':get_time()})

@connection.connection_handler
def edit_subcomment(cursor,id_,message):
    cursor.execute("""
    UPDATE comment 
    SET edited_count = edited_count + 1, message = %(msg)s
    WHERE id = %(id)s
    """, {'id':id_, 'msg':message})

@connection.connection_handler
def add_answer(cursor,message, image,question_id):

    submission_time = get_time()
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
def delete_subcomment(cursor,id_):
    cursor.execute('DELETE FROM comment WHERE id = %(id)s', {'id':id_})

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

@connection.connection_handler
def search_engine(cursor, search_phrase):
    cursor.execute("""
    SELECT * FROM question
    WHERE question.title ILIKE %(object)s OR question.message ILIKE %(object)s;
    """,
                   {'object': f'%{search_phrase}%'})
    searched_questions = cursor.fetchall()
    return searched_questions

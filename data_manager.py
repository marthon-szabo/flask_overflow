from psycopg2 import sql
import connection
from datetime import datetime
import server
import bcrypt

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

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
def add_question(cursor,title,message,image,tagid):

    submission_time = get_time()
    user_id = server.get_user_id()
    cursor.execute("""
        INSERT INTO question
        (title, message, image, submission_time, view_number, vote_number,user_id)
        VALUES (%(title)s,%(message)s,%(image)s,%(submission_time)s,0,0,%(user_id)s)
    """,{'title':title, 'message':message, 'image':image, 'submission_time':submission_time,'user_id':user_id}
    )
    cursor.execute("""
        SELECT MAX(id) FROM question
    """)
    question_id = cursor.fetchone()['max']

    cursor.execute("""
        INSERT INTO question_tag
        (question_id, tag_id)
        VALUES(%(qid)s, %(tid)s) 
    """, {'qid':question_id, 'tid':tagid})

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
    user_id = server.get_user_id()
    cursor.execute("""
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count,user_id)
    VALUES (%(question_id)s, NULL, %(message)s, %(timenow)s, 0 ,%(user_id)s)
    """, {'question_id':question_id, 'message':message, 'timenow':get_time(), 'user_id':user_id})

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
    user_id = server.get_user_id()
    cursor.execute("""
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count,user_id)
    VALUES (NULL, %(id_)s, %(msg)s, %(timenow)s, 0,%(user_id)s)
    """, {'id_':answer_id, 'msg':message, 'timenow':get_time(), 'user_id':user_id})

@connection.connection_handler
def edit_subcomment(cursor,id_,message):
    cursor.execute("""
    UPDATE comment 
    SET edited_count = edited_count + 1, message = %(msg)s
    WHERE id = %(id)s
    """, {'id':id_, 'msg':message})

@connection.connection_handler
def add_answer(cursor,message, image,question_id):
    user_id = server.get_user_id()
    submission_time = get_time()
    cursor.execute("""
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, image,user_id)
        VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s, %(user_id)s);
    """,{'submission_time':submission_time,'question_id':question_id, 'message':message,'image':image, 'user_id':user_id})

@connection.connection_handler
def get_user_answer_likes(cursor,answer_id,user_id):
    cursor.execute("""
        SELECT * FROM user_votes
        WHERE answer_id = %(aid)s
        AND user_id = %(uid)s
    """, {'aid':answer_id, 'uid':user_id})
    return cursor.fetchone()

@connection.connection_handler
def add_vote_to_answer(cursor, answer_id, value):
    cursor.execute("""
        UPDATE answer
        SET vote_number = vote_number + %(v)s
        WHERE id = %(id)s
    """,{'v':value, 'id':answer_id})

@connection.connection_handler
def like_post(cursor,id_, user_id): #like answer
    like = get_user_answer_likes(id_, user_id)
    if like:
        if like['vote_type'] == 1: #Ha már likeolta
            add_vote_to_answer(id_, -1)
            remove_user_vote(user_id, 0, id_)
        else: #Ha downvoteolta
            add_vote_to_answer(id_, 2) #Downvote disable + 1 vote
            update_user_vote_type(user_id, 1, 0, id_)
    else:
        add_vote_to_answer(id_, 1)
        add_user_vote(user_id,0,id_,1)

@connection.connection_handler
def dislike_post(cursor,answer_id, user_id): #dislike answer
    like = get_user_answer_likes(answer_id, user_id)
    if like:
        if like['vote_type'] == -1:
            add_vote_to_answer(answer_id, 1)
            remove_user_vote(user_id, 0, answer_id)
        else:
            add_vote_to_answer(answer_id, -2)
            update_user_vote_type(user_id, -1, 0, answer_id)
    else:
        add_user_vote(user_id, 0, answer_id, -1)
        add_vote_to_answer(answer_id, -1)

@connection.connection_handler
def add_vote_to_question(cursor, question_id, value):
    cursor.execute("""
        UPDATE question
        SET vote_number = vote_number + %(value)s
        WHERE id = %(qid)s
    """, {'value':value, 'qid':question_id})

@connection.connection_handler
def remove_user_vote(cursor, user_id, question_id,answer_id):
    cursor.execute("""
        DELETE FROM user_votes
        WHERE user_id = %(id)s
        AND question_id = %(qid)s
        AND answer_id = %(aid)s
    """, {'id':user_id, 'qid':question_id, 'aid':answer_id})

@connection.connection_handler
def update_user_vote_type(cursor, user_id, type, question_id, answer_id):
    cursor.execute("""
        UPDATE user_votes
        SET vote_type = %(type)s
        WHERE user_id = %(uid)s
        AND question_id = %(qid)s
        AND answer_id = %(aid)s   
    """, {'type':type, 'qid':question_id, 'aid':answer_id, 'uid':user_id})

@connection.connection_handler
def add_user_vote(cursor,user_id, question_id, answer_id, vote_type):
    cursor.execute("""
        INSERT INTO user_votes
        (user_id, answer_id, question_id, vote_type)
        VALUES(%(uid)s,%(answer_id)s, %(qid)s, %(vtype)s) 
    """, {'uid':user_id, 'answer_id':answer_id ,'qid':int(question_id), 'vtype':int(vote_type)})

@connection.connection_handler
def like_question(cursor,id_, user_id):
    if user_id > 0:
        cursor.execute("""
            SELECT * FROM user_votes
            WHERE question_id = %(id)s
            AND user_id = %(userid)s
        """, {'id':id_, 'userid':user_id})
        likes = cursor.fetchone()

        if likes:
            if int(likes['vote_type']) == 1:  #Ha már van rajta egy like
                add_vote_to_question(id_, -1)  #Szedje le róla
                remove_user_vote(user_id, id_, 0) # Törölje a user vote-ját
            else:  # HA downvote van rajta
                add_vote_to_question(id_, 2) #Adjon hozzá 2 lájkot ( downvote eltüntetés + 1 like )
                update_user_vote_type(user_id,1,id_,0)
        else:
            add_vote_to_question(id_, 1)
            add_user_vote(user_id, id_,0, 1)

@connection.connection_handler
def dislike_question(cursor, id_, user_id):
    if user_id > 0:
        cursor.execute("""
            SELECT * FROM user_votes
            WHERE question_id = %(id)s
            AND user_id = %(userid)s
        """, {'id':id_, 'userid':user_id})
        likes = cursor.fetchone()
        if likes:
            if likes['vote_type'] == -1: #Ha dislikeolta
                remove_user_vote(user_id, id_, 0)  #Törölje a dbből
                add_vote_to_question(id_, 1) #Nullázza a downvote-t
            else:  #Ha likeolta
                update_user_vote_type(user_id, -1,id_,0) #Downvotera állitsa
                add_vote_to_question(id_, -2) # Vegye le likeot + dislike
        else:
            add_user_vote(user_id, id_,0, -1)
            add_vote_to_question(id_, -1)

@connection.connection_handler
def view_question(cursor, id_, user_id):
    if user_id == 0:
        return

    cursor.execute("""
        SELECT * FROM user_views
        WHERE user_id = %(user)s
        AND question_id = %(id)s
    """,{'user':user_id, 'id':id_})

    views = cursor.fetchall()
    if len(views) == 0:
        cursor.execute("""
            UPDATE question
            SET view_number = view_number + 1
            WHERE id = %(id)s;
        """, {'id':id_})

        cursor.execute("""
        INSERT INTO user_views
        (user_id, question_id)
        VALUES (%(user_id)s, %(id)s) 
        """, {'user_id':user_id, 'id':id_})

@connection.connection_handler
def delete_anwser(cursor,id_):
    cursor.execute("""ALTER TABLE answer DISABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE comment DISABLE TRIGGER ALL;""")
    cursor.execute("""
        DELETE FROM answer
        WHERE id = %(id)s;
        """, {'id': id_})

    cursor.execute("""
        DELETE FROM comment
        WHERE answer_id = %(id)s;
    """, {'id':id_})

    cursor.execute("""ALTER TABLE answer ENABLE TRIGGER ALL;""")
    cursor.execute("""ALTER TABLE comment ENABLE TRIGGER ALL;""")

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
    WHERE title ILIKE %(object)s OR message ILIKE %(object)s;
    """,
                   {'object': f'%{search_phrase}%'})
    searched_questions = cursor.fetchall()
    return searched_questions

@connection.connection_handler
def edit_answer(cursor, id_, message, image):
    cursor.execute("""
    UPDATE answer 
    SET  message = %(message)s, image = %(image)s
    WHERE id = %(id)s;
    """,{'message':message, 'image':image, 'id':id_}
    )


@connection.connection_handler
def get_answer(cursor, id_):
    cursor.execute("""
    SELECT * FROM answer
    WHERE id = %(id)s;
    """,{'id':id_})
    return cursor.fetchone()


@connection.connection_handler
def add_tag(cursor, name):
    cursor.execute("""
                    INSERT INTO tag (name) VALUES  (%(name)s)
                    """, {"name": name})


@connection.connection_handler
def view_tags(cursor, question_id):
    cursor.execute("""
        SELECT tag_id FROM question_tag
        WHERE question_id = %(id)s
    """, {'id':question_id})

    finded = cursor.fetchone()
    tag_id = finded['tag_id']

    cursor.execute("""
                    SELECT name FROM tag 
                    WHERE id = %(id)s""", {"id": tag_id})
    return cursor.fetchone()

@connection.connection_handler
def add_tag_to_question(cursor,question_id,tag_id):
    cursor.execute("""
                    INSERT INTO question_tag (tag_id,question_id)
                    VALUES(%(tid)s, %(qid)s)
                    """, {"tid": tag_id, "qid": question_id})

@connection.connection_handler
def edit_question_tag(cursor,question_id,tag_id):
    cursor.execute("""
    UPDATE question_tag
    SET tag_id = %(id)s
    WHERE question_id = %(qid)s
    """, {'id':tag_id, 'qid':question_id})


@connection.connection_handler
def view_all_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag""")
    return cursor.fetchall()

@connection.connection_handler
def delete_question_tag(cursor, id):
    cursor.execute("""
    DELETE FROM public.question_tag WHERE id = """)


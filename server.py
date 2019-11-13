import connection
from flask import Flask, request, render_template,redirect

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('mainpage.html')

@app.route('/send_comment/<int:question_id>', methods=['GET','POST'])
def send_comment(question_id):
    if request.form['my_comment'].replace(' ', '') != '':
        connection.add_answer(request.form['my_comment'],request.form['image_link'],question_id)
    return display_question(question_id, False)
    #return redirect('/question/' + str(question_id))

@app.route('/vote_anwser<int:question_id><int:comment_id>', methods=['GET','POST'])
def vote_anwser(question_id,comment_id):
    connection.like_post(comment_id)
    return display_question(question_id, False)
    #return redirect('/question/'+str(question_id))

@app.route('/upvote_question<int:question_id>', methods=['GET','POST'])
def upvote_question(question_id):
    connection.like_question(question_id)
    return display_question(question_id, False)
    #return redirect('/question/'+str(question_id))

@app.route('/delete_anwser<int:question_id><int:comment_id>', methods=['GET','POST'])
def delete_anwser(question_id, comment_id):
    connection.delete_anwser(comment_id)
    return display_question(question_id, False)

@app.route('/delete_question<int:question_id>', methods=['GET','POST'])
def delete_question(question_id):
    connection.delete_question(question_id)
    return listing_questions()

@app.route('/devote_anwser<int:question_id><int:comment_id>', methods=['GET','POST'])
def devote_anwser(question_id,comment_id):
    connection.dislike_post(comment_id)
    return display_question(question_id, False)
    #return redirect('/question/'+str(question_id))

@app.route('/downvote_question<int:question_id>', methods=['GET','POST'])
def downvote_question(question_id):
    connection.dislike_question(question_id)
    return display_question(question_id,False)
    #return redirect('/question/'+str(question_id))

@app.route('/list')
def listing_questions():
    return render_template("list.html", questions=connection.questions)

@app.route('/question/<int:question_id>', methods=['GET','POST'])
def display_question(question_id, plus_view=True):
    for record in connection.questions:
        if int(record['id']) == question_id:
            if plus_view:
                connection.view_question(question_id)
            return render_template('display_question.html', question_id=question_id, questions = connection.questions, max_voted = connection.get_max_voted(question_id) ,anwsers = sorted(connection.answers, key=lambda k: int(k['vote_number'])) )
    return redirect('/list')

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        connection.add_question(request.form["new_question"], request.form["message"], request.form["image"])
        return redirect("/list")
    return render_template("add_question.html", questions = connection.questions)


if __name__ == "__main__":
    connection.read_answers()
    connection.read_questions()
    app.run(
        debug=True, # Allow verbose error reports
        port=6969 # Set custom port
    )

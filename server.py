import connection

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('mainpage.html')

@app.route('/vote_anwser<int:question_id><int:comment_id>', methods=['GET','POST'])
def vote_anwser(question_id,comment_id):
    connection.like_post(comment_id)
    return  display_question(question_id)

@app.route('/list')
def listing_questions():
    return render_template("list.html", questions=connection.questions)

@app.route('/question/<int:question_id>', methods=['GET','POST'])
def display_question(question_id):
	return render_template('display_question.html', question_id=question_id, questions = connection.questions, anwsers = connection.answers)

@app.route('/add-question')
def add_question():
	pass


@app.route('/question/<question_id>/new-answer')
def add_answer():
	pass


if __name__ == "__main__":
    connection.read_answers()
    connection.read_questions()
    app.run(
        debug=True, # Allow verbose error reports
        port=6969 # Set custom port
    )

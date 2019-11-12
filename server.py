import connection

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('mainpage.html')


@app.route('/list')
def listing_questions():
	return render_template('/mainpage.html')


@app.route('/question/<int:question_id>')
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
    connection.add_question('asd','keci','fos')
    app.run(
        debug=True, # Allow verbose error reports
        port=6969 # Set custom port
    )

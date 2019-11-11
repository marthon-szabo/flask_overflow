from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('mainpage.html')


@app.route('/list')
def listing_questions():
	pass


@app.route('/question/<question_id>')
def display_question():
	pass


@app.route('/add-question')
def add_question():
	pass


@app.route('/question/<question_id>/new-answer')
def add_answer():
	pass


if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=6969 # Set custom port
    )

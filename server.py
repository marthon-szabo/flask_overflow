from flask import Flask, request,

app = Flask(__name__)

@app.route('/list')
	def listing_questions():
		pass


@app.route('//question/<question_id>')
	def display_question():
		pass


@app.route('/add-question')
	def add_question():
		pass


@app.route('/question/<question_id>/new-answer')
	def add_answer():
		pass

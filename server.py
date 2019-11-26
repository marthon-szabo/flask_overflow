import data_manager
from flask import Flask, request, render_template,redirect

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main_page():
    table = data_manager.get_latest_questions()
    return render_template('list.html', questions = table)

@app.route('/send_comment/<int:question_id>', methods=['GET','POST'])
def send_comment(question_id):
    if request.form['my_comment'].replace(' ', '') != '':
        data_manager.add_answer(request.form['my_comment'],request.form['image_link'],question_id,data_manager.get_time())
    return redirect('/question/' + str(question_id) + "/1")

@app.route('/send_subcomment_to_question/<int:question_id>', methods = ['POST'])
def send_subcomment_to_question(question_id):
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_subbcomment_to_question(question_id, message)
    return redirect('/question/' + str(question_id) + "/1")

@app.route('/send_subcomment_to_answer/<int:answer_id>/<int:question_id>', methods = ['POST'])
def send_subcomment_to_anwser(answer_id, question_id):
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_subbcomment_to_answer(answer_id,message)
    return redirect('/question/' + str(question_id) + '/1')

@app.route('/vote_anwser<int:question_id>/<int:comment_id>', methods=['GET','POST'])
def vote_anwser(question_id,comment_id):
    data_manager.like_post(comment_id)
    return redirect('/question/' + str(question_id) + "/1")

@app.route('/upvote_question<int:question_id>', methods=['GET','POST'])
def upvote_question(question_id):
    data_manager.like_question(question_id)
    return redirect('/question/' + str(question_id) + "/1")

@app.route('/delete_anwser<int:question_id>/<int:comment_id>', methods=['GET','POST'])
def delete_anwser(question_id, comment_id):
    data_manager.delete_anwser(comment_id)
    return redirect('/question/'+str(question_id)  + "/1")

@app.route('/delete_question<int:question_id>', methods=['GET','POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return listing_questions()

@app.route('/edit_subcomment/<int:comment_id>/<int:question_id>', methods=['GET', 'POST'])
def edit_subcomment(comment_id, question_id):
    if request.method == 'POST':
        data_manager.edit_subcomment(comment_id, request.form['message'])
        return redirect('/question/' + str(question_id) + '/1')
    return render_template('edit_subcomment.html', comment_id = comment_id, question_id = question_id, subcomments = data_manager.get_subcomments())

@app.route('/devote_anwser<int:question_id>/<int:comment_id>', methods=['GET','POST'])
def devote_anwser(question_id,comment_id):
    data_manager.dislike_post(comment_id)
    return redirect('/question/'+str(question_id) + "/1")

@app.route('/downvote_question<int:question_id>', methods=['GET','POST'])
def downvote_question(question_id):
    data_manager.dislike_question(question_id)
    return redirect('/question/' + str(question_id) + "/1")

@app.route('/list', methods=['GET','POST'])
def listing_questions():
    table = data_manager.get_questions()
    return render_template('list.html', questions = table, selected = 'Heat')

@app.route('/slist', methods=['GET', 'POST'])
def sort_questions():
    table = data_manager.sort_question_by(request.args.get('order_by'),request.args.get('order_direction'))
    return render_template('list.html', questions = table, selected = 'Heat')

@app.route('/question/<int:question_id>/<plus_view>', methods=['GET','POST'])
def display_question(question_id, plus_view="0"):
    for record in data_manager.get_questions():
        if int(record['id']) == question_id:
            if plus_view == "0":
                data_manager.view_question(question_id)
            try:
                max_vote = int(data_manager.get_max_like(question_id))
            except:
                max_vote = 0
            return render_template('display_question.html', question_id=question_id, question = data_manager.get_question(question_id), max_voted = max_vote ,anwsers = data_manager.get_answers(question_id), comments = data_manager.get_subcomments())
    return redirect('/list')

@app.route('/delete-subcomment/<int:comment_id>/<int:question_id>', methods = ['GET', 'POST'])
def delete_subcomment(comment_id, question_id):
    data_manager.delete_subcomment(comment_id)
    return render_template('display_question.html', question_id=question_id,
                           question=data_manager.get_question(question_id), max_voted=1,
                           anwsers=data_manager.get_answers(question_id), comments=data_manager.get_subcomments())


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        #connection.add_question(request.form["new_question"], request.form["message"], request.form["image"])
        data_manager.add_question(request.form['new_question'], request.form['message'], request.form['image'], data_manager.get_time())
        return redirect("/list")
    return render_template("add_question.html", questions = data_manager.get_questions())

@app.route('/edit-question/<int:question_id>', methods=["GET", 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        #connection.edit_question(question_id, request.form["title"], request.form["message"], request.form["image"])
        data_manager.edit_question(question_id,request.form['title'], request.form['message'], request.form['image'])
        return redirect('/question/' + str(question_id) + "/1")
    return render_template('edit_question.html', question_id=question_id, questions=data_manager.get_questions())

@app.route('/super-secret', methods=['GET','POST'])
def super_secret():
    return render_template("rickross.html")

if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=6969 # Set custom port
    )
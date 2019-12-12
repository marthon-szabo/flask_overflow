from flask import Flask, request, render_template, redirect, session, g, escape, url_for
import data_manager

app = Flask(__name__)
app.secret_key = 'Tilted Towers'

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']
    return g.user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uname = request.form['uname']
        pw = request.form['pw']
        hashed_pw = data_manager.get_hash_pw(uname, pw)
        user_id = data_manager.get_id(uname)
        verification = None
        if verification == None:
            verification = False
        else:
            verification = data_manager.verify_password(pw, hashed_pw)
        if verification:
            session['user_id'] = user_id
            session['theme'] = request.form['theme']
            return redirect(url_for('main_page'))
        else:
            return render_template('login.html', verification=verification)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        uname = request.form['uname']
        pw = request.form['pw']
        c_pw = request.form['c_pw']
        email = request.form['email']
        users_and_emails = data_manager.get_email()
        is_email = data_manager.is_same_email(email, users_and_emails)
        is_same_pw = data_manager.is_same_pw(pw, c_pw)
        is_username = data_manager.is_same_username(uname, users_and_emails)
        if is_same_pw == 'True':
            return render_template('register.html', is_same_pw=is_same_pw)
        if is_username == 'True':
            return render_template('register.html', is_username=is_username)

        if is_email == 'True':
            return render_template('register.html', is_email=is_email)
        else:
            hashed_pw = data_manager.hash_password(pw)
            if request.form.get('gender'):
                gender = 'Male'
                data_manager.add_user(uname, hashed_pw, email, gender)
                return redirect(url_for('login'))
            else:
                gender = 'Female'
                data_manager.add_user(uname, hashed_pw, email, gender)
                return redirect(url_for('login'))



@app.route('/', methods=['GET', 'POST'])
def main_page():
    table = data_manager.get_latest_questions()
    user_s = escape(session['username'])
    return render_template('list.html', questions=table, user_s=user_s)


@app.route('/send_comment/<int:question_id>', methods=['GET', 'POST'])
def send_comment(question_id):
    if request.form['my_comment'].replace(' ', '') != '':
        data_manager.add_answer(request.form['my_comment'], request.form['image_link'], question_id)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/send_subcomment_to_question/<int:question_id>', methods=['POST'])
def send_subcomment_to_question(question_id):
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_subbcomment_to_question(question_id, message)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/send_subcomment_to_answer/<int:answer_id>/<int:question_id>', methods=['POST'])
def send_subcomment_to_anwser(answer_id, question_id):
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_subbcomment_to_answer(answer_id, message)
    return redirect('/question/' + str(question_id) + '/1')


@app.route('/vote_anwser<int:question_id>/<int:comment_id>', methods=['GET', 'POST'])
def vote_anwser(question_id, comment_id):
    data_manager.like_post(comment_id)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/upvote_question<int:question_id>', methods=['GET', 'POST'])
def upvote_question(question_id):
    data_manager.like_question(question_id)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/delete_anwser<int:question_id>/<int:comment_id>', methods=['GET', 'POST'])
def delete_anwser(question_id, comment_id):
    data_manager.delete_anwser(comment_id)
    # return display_question(question_id, False)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/delete_question<int:question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return listing_questions()


@app.route('/edit_subcomment/<int:comment_id>/<int:question_id>', methods=['GET', 'POST'])
def edit_subcomment(comment_id, question_id):
    if request.method == 'POST':
        data_manager.edit_subcomment(comment_id, request.form['message'])
        return redirect('/question/' + str(question_id) + '/1')
    return render_template('edit_subcomment.html', comment_id=comment_id, question_id=question_id,
                           subcomments=data_manager.get_subcomments())


@app.route('/devote_anwser<int:question_id>/<int:comment_id>', methods=['GET', 'POST'])
def devote_anwser(question_id, comment_id):
    data_manager.dislike_post(comment_id)
    # return display_question(question_id, False)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/downvote_question<int:question_id>', methods=['GET', 'POST'])
def downvote_question(question_id):
    data_manager.dislike_question(question_id)
    # return display_question(question_id,False)
    return redirect('/question/' + str(question_id) + "/1")


@app.route('/list', methods=['GET', 'POST'])
def listing_questions():
    if request.method == 'POST':
        search = request.form.get('search-field')
        search = search.lower()
        if " " in search:
            table = data_manager.get_questions()
            return render_template('list.html', questions=table, search=search, selected='Heat')
        elif search:
            searched_questions = data_manager.search_engine(search)
            marked = []
            for word in searched_questions:
                lowered = word['title'].lower()
                for i in lowered.split():
                    if search == i:
                        print('True')

                    print(searched_questions)
                    return render_template('list.html', searched_questions=searched_questions)
        else:
            searched_questions = data_manager.search_engine(search)
            print(searched_questions)
            return render_template('list.html', searched_questions=searched_questions)

    else:
        table = data_manager.get_questions()
        return render_template('list.html', questions=table, selected='Heat')


@app.route('/slist', methods=['GET', 'POST'])
def sort_questions():
    table = data_manager.sort_question_by(request.args.get('order_by'), request.args.get('order_direction'))
    return render_template('list.html', questions=table, selected='Heat')


@app.route('/question/<int:question_id>/<plus_view>', methods=['GET', 'POST'])
def display_question(question_id, plus_view="0"):
    get_answers = data_manager.get_answers(question_id)
    print(get_answers)
    questions = data_manager.get_questions()
    for record in questions:
        if int(record['id']) == question_id:
            if plus_view == "0":
                data_manager.view_question(question_id)
            try:
                max_vote = int(data_manager.get_max_like(question_id))
            except:
                max_vote = 0
            return render_template('display_question.html', question_id=question_id,
                                   question=data_manager.get_question(question_id), max_voted=max_vote,
                                   anwsers=data_manager.get_answers(question_id),
                                   comments=data_manager.get_subcomments(),
                                   qcomments=data_manager.get_question_subcomments(question_id),
                                   tag=data_manager.view_tags(question_id))
    return redirect('/list')


@app.route('/delete-subcomment/<int:comment_id>/<int:question_id>', methods=['GET', 'POST'])
def delete_subcomment(comment_id, question_id):
    data_manager.delete_subcomment(comment_id)
    return redirect('/question/' + str(question_id) + '/1')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        data_manager.add_question(request.form["new_question"], request.form["message"], request.form["image"],
                                  request.form['title'])
        return redirect("/list")
    return render_template("add_question.html", questions=data_manager.get_questions(),
                           tags=data_manager.view_all_tags())


@app.route('/edit-question/<int:question_id>', methods=["GET", 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager.edit_question(question_id, request.form["title"], request.form["message"], request.form["image"])
        return redirect('/question/' + str(question_id) + "/1")
    return render_template('edit_question.html', question_id=question_id, questions=data_manager.get_questions())


@app.route('/super-secret', methods=['GET', 'POST'])
def super_secret():
    session['user_id'] = 1
    session['theme'] = 'Terraria'
    # return render_template("rickross.html")


def get_user_id():
    if session['user_id']:
        return session['user_id']
    return 0


@app.route('/edit-answer/<int:question_id>/<int:answer_id>', methods=["GET", 'POST'])
def edit_answer(question_id, answer_id):
    answer = data_manager.get_answer(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(answer_id, request.form["message"], request.form["image"])
        return redirect('/question/' + str(question_id) + "/1")
    return render_template('edit-answer.html', answer_id=answer_id, answer=answer, question_id=question_id)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'POST':
        tag_id = request.form['tagid']
        # tag_name = data_manager.add_tag(name)
        data_manager.edit_question_tag(question_id, tag_id)
        return redirect('/question/' + str(question_id) + '/1')
    return render_template('new_tag.html', question_id=question_id, tags=data_manager.view_all_tags())


@app.route('/create-tag-then-return', methods=['POST'])
def create_and_return():
    data_manager.add_tag(request.form['title'])
    return redirect('/add-question')


@app.route('/create-tag', methods=["POST"])
def create_tag():
    data_manager.add_tag(request.form['title'])
    question_id = request.form['question_id']
    return redirect('/question/' + str(question_id) + '/new-tag')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=6969  # Set custom port
    )

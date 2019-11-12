with open("/home/skogmaan/Documents/flask_overflow/sample_data/question.csv", "r+") as text:


    def read_text(file_name):
        questions = file_name.readlines()
        questions = [line.strip("\n") for line in questions]
        print(questions)
        question_lines = []
        for lines in questions:
            question = lines.split(",")
            question_lines.append(question)
        question_lines = [line for line in question_lines if line != ['']]
        print(question_lines)

        titles = question_lines[0]
        print(titles)
        titles_with_questions = [(key, value) for key, value in zip(titles, question_lines)]
        print(titles_with_questions)


    read_text(text)
"""
    questions = text.readlines()
    question_lines = []
    titles = []
    for lines in questions:
        questions = lines.split(",")
        if "\n" in questions:
            lines.replace("\n", "")
        question_lines.append(questions)
    titles.append(question_lines[0])

    print(titles)


    questions_with_tags = {key for key in titles[0]}
    print(questions_with_tags)
"""

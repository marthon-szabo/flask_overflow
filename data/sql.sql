DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS question_tag;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS comment;


CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    title character varying(255) NOT NULL,
    message character varying(255) NOT NULL,
    image character varying(100) NOT NULL,
    submission_time integer NOT NULL,
    view_number integer NOT NULL,
    vote_number integer NOT NULL
);

CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

CREATE TABLE tag(
    id SERIAL PRIMARY KEY,
    name character varying(255)
);

CREATE TABLE answer  (
   id SERIAL PRIMARY KEY,
   submission_time integer NOT NULL,
   vote_number integer NOT NULL,
   question_id integer NOT NULL,
   message character varying(255) NOT NULL,
   image character varying(255)
);

CREATE TABLE comment  (
   id SERIAL PRIMARY KEY,
   answer_id integer NOT NULL,
   submission_time integer NOT NULL,
   question_id integer NOT NULL,
   message character varying(255) NOT NULL,
   edited_number integer NOT NULL
);



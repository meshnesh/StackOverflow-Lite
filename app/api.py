from app import app
from flask import request , jsonify, json
from app.models import Answer, Question

all_questions = []
all_answers = []

@app.route("/",methods=["GET"])
def home():

     return jsonify({"endpoints":[
         {'Get all questions': "/api/v1/question GET"},
         {'Get a single question':"/api/v1/questions/<question_id> GET"},
         {'Post question':"/api/v1/questions POST"},
         {'Post Answer':"/api/v1/questions/<question_id>/answer POST"}
         ]})


@app.route("/api/v1/questions", methods=["GET"])
# fetching all questions
def get_all_questions():
    if len(all_questions) > 0:
        return jsonify({
            "message":"Successfully viewed Questions",
            "Available questions":[     
                question.__dict__ for question in all_questions
            ]
        }),200
    return jsonify({"message":"No Question has been posted yet"}), 404


@app.route("/api/v1/questions/<question_id>", methods=["GET"])
# get a specific question
def get_a_question(question_id):
    _id = question_id.strip()
    
    for question in range(len(all_questions)):
        if ((all_questions[question]["qstn_id"]) == int(_id)):
            return jsonify({
            "message":"Successfully viewed Question",
            "Question":[     
                all_questions[question]["question"]
            ]
    }),200
    return jsonify({
        "message":"No such question is available",
    }),400

@app.route("/api/v1/questions", methods=["POST"])
# posting a single question
def post_question():
    data = request.get_json()
    question = data.get("question").strip()
    if not question:
        return jsonify({"message": "No input was given"}), 400
    qstn_id = len(all_questions) + 1
    new_question = Question(qstn_id , question)
    all_questions.append(new_question)
    return jsonify({"message":"New question successfully posted"}), 201


@app.route("/api/v1/questions/<question_id>/answer", methods=["POST"])
# answering a specific question
def post_answer(question_id):
    _id = question_id.strip()
    data = request.get_json()
    answer = data.get("answer")
    ans = answer.strip()

    for question in range(len(all_questions)):
        if ((all_questions[question]["qstn_id"]) == int(_id)):
            ans_id = len(all_answers) + 1
            new_answer = Answer(ans_id, ans, _id)
            all_answers.append(new_answer)
            return jsonify({
            "message":"Answer successfully posted to question",
            "Question answered":[     
                all_questions[question]["question"]
            ]}),201
    return jsonify({
        "message":"No such question is available",
    }),400




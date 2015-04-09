import os
import random
import string
import traceback

from flask import abort, Flask, jsonify, redirect, render_template, request, session, url_for
from flask.ext.cors import cross_origin
from flask.ext.sqlalchemy import SQLAlchemy

from aux import SECRET_KEY
from consts import DOMAINS, ISO_CODE_TO_COUNTRY_NAME, STRINGS_D, STORIES, SURVEYS, QUESTIONS

app = Flask(__name__)
app.secret_key = SECRET_KEY
# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

# # Models
# class Survey(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	consent = db.Column(db.Boolean)
# 	age = db.Column(db.String(32))
# 	gender = db.Column(db.String(32))
# 	education = db.Column(db.String(32))
# 	country_origin = db.Column(db.String(32))
# 	country_residence = db.Column(db.String(32))
# 	native_lang = db.Column(db.String(32))
# 	q1 = db.Column(db.Integer, nullable=True)
# 	q1_ans = db.Column(db.String(32), nullable=True)
# 	q2 = db.Column(db.Integer, nullable=True)
# 	q2_ans = db.Column(db.String(32), nullable=True)
# 	q3 = db.Column(db.Integer, nullable=True)
# 	q3_ans = db.Column(db.String(32), nullable=True)
# 	q4 = db.Column(db.Integer, nullable=True)
# 	q4_ans = db.Column(db.String(32), nullable=True)
# 	q5 = db.Column(db.Integer, nullable=True)
# 	q5_ans = db.Column(db.String(32), nullable=True)
# 	q6 = db.Column(db.Integer, nullable=True)
# 	q6_ans = db.Column(db.String(32), nullable=True)
# 	q7 = db.Column(db.Integer, nullable=True)
# 	q7_ans = db.Column(db.String(32), nullable=True)
# 	q8 = db.Column(db.Integer, nullable=True)
# 	q8_ans = db.Column(db.String(32), nullable=True)
# 	q9 = db.Column(db.Integer, nullable=True)
# 	q9_ans = db.Column(db.String(32), nullable=True)
# 	q10 = db.Column(db.Integer, nullable=True)
# 	q10_ans = db.Column(db.String(32), nullable=True)
# 	q11 = db.Column(db.Integer, nullable=True)
# 	q11_ans = db.Column(db.String(32), nullable=True)
# 	q12 = db.Column(db.Integer, nullable=True)
# 	q12_ans = db.Column(db.String(32), nullable=True)
# 	q13 = db.Column(db.Integer, nullable=True)
# 	q13_ans = db.Column(db.String(32), nullable=True)
# 	q14 = db.Column(db.Integer, nullable=True)
# 	q14_ans = db.Column(db.String(32), nullable=True)
# 	q15 = db.Column(db.Integer, nullable=True)
# 	q15_ans = db.Column(db.String(32), nullable=True)
# 	q16 = db.Column(db.Integer, nullable=True)
# 	q16_ans = db.Column(db.String(32), nullable=True)
# 	q17 = db.Column(db.Integer, nullable=True)
# 	q17_ans = db.Column(db.String(32), nullable=True)
# 	q18 = db.Column(db.Integer, nullable=True)
# 	q18_ans = db.Column(db.String(32), nullable=True)
# 	q19 = db.Column(db.Integer, nullable=True)
# 	q19_ans = db.Column(db.String(32), nullable=True)
# 	q20 = db.Column(db.Integer, nullable=True)
# 	q20_ans = db.Column(db.String(32), nullable=True)
# 	q21 = db.Column(db.Integer, nullable=True)
# 	q21_ans = db.Column(db.String(32), nullable=True)
# 	q22 = db.Column(db.Integer, nullable=True)
# 	q22_ans = db.Column(db.String(32), nullable=True)
# 	q23 = db.Column(db.Integer, nullable=True)
# 	q23_ans = db.Column(db.String(32), nullable=True)
# 	confirmation_code = db.Column(db.String(32))
# 	confirmed = db.Column(db.Boolean)

# 	def __init__(self, consent, age, gender, education, country_origin,
# 				 country_residence, native_lang, confirmation_code):
# 		self.consent = consent
# 		self.age = age
# 		self.gender = gender
# 		self.education = education
# 		self.country_origin = country_origin
# 		self.country_residence = country_residence
# 		self.native_lang = native_lang
# 		self.confirmation_code = confirmation_code
# 		self.confirmed = False

# Routing
@app.route("/", methods=["GET"])
def main():
	return render_template("index.html")

@app.route("/set_lang/", methods=["POST"])
def set_lang():
	req_data = request.get_json()
	if "lang" not in req_data or (req_data["lang"] != "en" and req_data["lang"] != "chn"):
		abort(403)
	session["lang"] = req_data["lang"]
	return redirect(url_for("get_consent"))
	#return jsonify({"success": True})

@app.route("/get_consent/", methods=["GET"])
def get_consent():
	if "lang" not in session:
		return redirect(url_for("main"))
	return render_template("consent.html", lang=session["lang"],
										   strings_d=STRINGS_D)

@app.route("/set_consent/", methods=["POST"])
def set_consent():
	req_data = request.get_json()
	if "lang" not in session or "consent" not in req_data or type(req_data["consent"]) != bool:
		abort(403)
	if req_data["consent"]:
		session["consent"] = True
		return redirect(url_for("get_demographics"))
	else:
		session["consent"] = False
		return redirect(url_for("get_demographics"))

@app.route("/no_consent/", methods=["GET"])
def no_consent():
	return render_template("no_consent.html", lang=session["lang"],
											  strings_d=STRINGS_D)

@app.route("/get_demographics/", methods=["GET"])
def get_demographics():
	if "lang" not in session:
		return redirect(url_for("main"))
	elif "consent" not in session:
		return redirect(url_for("get_consent"))
	elif session["consent"] == False:
		return redirect(url_for("no_consent"))
	return render_template("demographics.html", lang=session["lang"],
												strings_d=STRINGS_D)

@app.route('/set_demographics/', methods=['POST'])
def set_demographics():
	req_data = request.get_json()
	print "req_data:", req_data
	if "consent" not in session or not session["consent"]:
		abort(403)
	if ('age' not in req_data or 'gender' not in req_data
		or 'education' not in req_data or 'country_origin' not in req_data
		or 'country_residence' not in req_data or 'native_lang' not in req_data):
		abort(403)
	session['age'] = req_data['age']
	session['gender'] = req_data['gender']
	session['education'] = req_data['education']
	session['country_origin'] = req_data['country_origin']
	session['country_residence'] = req_data['country_residence']
	session['native_lang'] = req_data['native_lang']
	session['demographics_complete'] = True
	print "session:", session
	# return render_template("quiz")
	# survey_data = get_survey_data()
	return ""
	# try:
	# 	return render_template('survey.html', survey_data=survey_data,
	# 									  	  code_to_name=ISO_CODE_TO_COUNTRY_NAME,
	# 									  	  lang=session['lang'],
	# 									  	  strings_d=STRINGS_D)
	# except:
	# 	print 'Unexpected error:'
	# 	traceback.print_exc()

@app.route("/quiz/", methods=["GET"])
def get_quiz():
	if "lang" not in session:
		return redirect(url_for("main"))
	elif "consent" not in session:
		return redirect(url_for("get_consent"))
	elif session["consent"] == False:
		return redirect(url_for("no_consent"))
	elif not session["demographics_complete"]:
		return redirect(url_for("get_demographics"))
	survey_data = get_quiz_data()
	return render_template('survey.html', survey_data=survey_data,
										  code_to_name=ISO_CODE_TO_COUNTRY_NAME,
										  lang=session['lang'],
										  strings_d=STRINGS_D)

# @app.route('/submit_quiz/', methods=['POST'])
# def submit_quiz():
# 	if 'demographics_complete' not in session or 'quiz_submitted' in session:
# 	# User hasn't completed the tool's demographics section, or the user has already
# 	# submitted a quiz instance.
# 		abort(403)

# 	form_data = request.form
# 	question_ids = request.form.keys()
# 	survey_id = None
# 	confirmation_code = None
# 	try:
# 		confirmation_code = gen_rand_code()
# 		survey = Survey(session['consent'], session['age'], session['gender'], session['education'],
# 						session['country_origin'], session['country_residence'], session['native_lang'],
# 						confirmation_code)
# 		if len(question_ids) >= 1:
# 			survey.q1 = int(question_ids[0])
# 			survey.q1_ans = form_data[question_ids[0]]
# 		if len(question_ids) >= 2:
# 			survey.q2 = int(question_ids[1])
# 			survey.q2_ans = form_data[question_ids[1]]
# 		if len(question_ids) >= 3:
# 			survey.q3 = int(question_ids[2])
# 			survey.q3_ans = form_data[question_ids[2]]
# 		if len(question_ids) >= 4:
# 			survey.q4 = int(question_ids[3])
# 			survey.q4_ans = form_data[question_ids[3]]
# 		if len(question_ids) >= 5:
# 			survey.q5 = int(question_ids[4])
# 			survey.q5_ans = form_data[question_ids[4]]
# 		if len(question_ids) >= 6:
# 			survey.q6 = int(question_ids[5])
# 			survey.q6_ans = form_data[question_ids[5]]
# 		if len(question_ids) >= 7:
# 			survey.q7 = int(question_ids[6])
# 			survey.q7_ans = form_data[question_ids[6]]
# 		if len(question_ids) >= 8:
# 			survey.q8 = int(question_ids[7])
# 			survey.q8_ans = form_data[question_ids[7]]
# 		if len(question_ids) >= 9:
# 			survey.q9 = int(question_ids[8])
# 			survey.q9_ans = form_data[question_ids[8]]
# 		if len(question_ids) >= 10:
# 			survey.q10 = int(question_ids[9])
# 			survey.q10_ans = form_data[question_ids[9]]
# 		if len(question_ids) >= 11:
# 			survey.q11 = int(question_ids[10])
# 			survey.q11_ans = form_data[question_ids[10]]
# 		if len(question_ids) >= 12:
# 			survey.q12 = int(question_ids[11])
# 			survey.q12_ans = form_data[question_ids[11]]
# 		if len(question_ids) >= 13:
# 			survey.q13 = int(question_ids[12])
# 			survey.q13_ans = form_data[question_ids[12]]
# 		if len(question_ids) >= 14:
# 			survey.q14 = int(question_ids[13])
# 			survey.q14_ans = form_data[question_ids[13]]
# 		if len(question_ids) >= 15:
# 			survey.q15 = int(question_ids[14])
# 			survey.q15_ans = form_data[question_ids[14]]
# 		if len(question_ids) >= 16:
# 			survey.q16 = int(question_ids[15])
# 			survey.q16_ans = form_data[question_ids[15]]
# 		if len(question_ids) >= 17:
# 			survey.q17 = int(question_ids[16])
# 			survey.q17_ans = form_data[question_ids[16]]
# 		if len(question_ids) >= 18:
# 			survey.q18 = int(question_ids[17])
# 			survey.q18_ans = form_data[question_ids[17]]
# 		if len(question_ids) >= 19:
# 			survey.q19 = int(question_ids[18])
# 			survey.q19_ans = form_data[question_ids[18]]
# 		if len(question_ids) >= 20:
# 			survey.q20 = int(question_ids[19])
# 			survey.q20_ans = form_data[question_ids[19]]
# 		if len(question_ids) >= 21:
# 			survey.q21 = int(question_ids[20])
# 			survey.q21_ans = form_data[question_ids[20]]
# 		if len(question_ids) >= 22:
# 			survey.q22 = int(question_ids[21])
# 			survey.q22_ans = form_data[question_ids[21]]
# 		db.session.add(survey)
# 		db.session.commit()
# 		survey_id = survey.id
# 		session['survey_submitted'] = True
# 	except:
# 		print 'Unexpected error:'
# 		traceback.print_exc()
# 	if not survey_id or not confirmation_code:
# 		try:
# 			return render_template('error.html', lang=session['lang'],
# 												 strings_d=STRINGS_D)
# 		except:
# 			print 'Unexpected error:'
# 			traceback.print_exc()
# 	else:
# 		try:
# 			return render_template('confirmation.html', confirmation_code=str(survey_id)+';'+confirmation_code,
# 														lang=session['lang'],
# 														strings_d=STRINGS_D)
# 		except:
# 			print 'Unexpected error:'
# 			traceback.print_exc()

# # @app.route('/validate_survey_completion', methods=['POST'])
# # @cross_origin()
# # def validate_survey_completion():
# # 	data = request.get_json()
# # 	if 'confirmation_code' not in data:
# # 		return jsonify({'success': False})
# # 	confirmation_code = data['confirmation_code']
# # 	confirmation_code_split = confirmation_code.split(';')
# # 	if len(confirmation_code_split) == 2:
# # 		identifier, code = confirmation_code_split
# # 		query_result = (db.session.query(Survey).filter(Survey.id == identifier)).first()
# # 		if query_result and query_result.confirmation_code == code and not query_result.confirmed:
# # 			query_result.confirmed = True
# # 			db.session.commit()
# # 			return jsonify({'success': True, 'confirmation_code': confirmation_code})
# # 		else:
# # 			return jsonify({'success': False})
# # 	else:
# # 		return jsonify({'success': False})

def get_quiz_data():
	"""
	Returns a list of dicts, where each dict's data characterizes a quiz question,
	such that the list characterizes a quiz instance where the ith dict in the list
	represents the ith question in the quiz.

	The data within each dict includes:
	- the id and text of a news story, and
	- a set of exactly four answer choices.
	"""
	survey_data = []
	for i in xrange(1, 23):
		survey_datum = {}
		survey_question_data = dict(QUESTIONS[i])
		survey_datum['question_id'] = i
		survey_datum['qid'] = i
		survey_datum['answer_choices'] = list(survey_question_data['choices'])
		if session['lang'] == 'en':
			survey_question_story = STORIES[survey_question_data['story_id']]['english_rewrite']
		else:
			survey_question_story = (STORIES[survey_question_data['story_id']]['chinese_rewrite']).decode('UTF-8')
		survey_datum['story'] = survey_question_story
		survey_data.append(survey_datum)
	print 'survey_data:', survey_data
	return survey_data
	# for domain in DOMAINS:
	# For each domain, we want 2 questions, each with 0.5-0.5 probability of
	# concerning a positive- or negative-valenced story.
		# question_data = {}
		# if random() < 0.5:
			# insert positive-valence story about domain into
		# else:
			# we're focusing on a negative-valence story about the domain
		# get choices

# 			# Add a positive-valence question regarding this domain
# 			# Add a negative-valence question regarding this domain
# 	survey_question_ids = list(SURVEYS[survey_num])
# 	random.shuffle(survey_question_ids)
# 	survey_question_ids.insert(6, 645)
# 	survey_question_ids.insert(15, 646)
# 	survey_data = []
# 	for question_id in survey_question_ids:
# 		survey_datum = {}
# 		survey_question_data = dict(QUESTIONS[question_id])

# 		survey_datum['question_id'] = question_id
# 		survey_question_answer_choices = list(survey_question_data['choices'])
# 		random.shuffle(survey_question_answer_choices)
# 		survey_datum['answer_choices'] = survey_question_answer_choices
		# if session['lang'] == 'en':
		# 	survey_question_story = STORIES[survey_question_data['story_id']]['english_rewrite']
		# else:
		# 	survey_question_story = (STORIES[survey_question_data['story_id']]['chinese_rewrite']).decode('UTF-8')
# 		survey_datum['story'] = survey_question_story

# 		survey_data.append(survey_datum)
# 	return survey_data

if __name__ == '__main__':
	app.run(debug=True)

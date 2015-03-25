import os
import random
import string
import traceback

from flask import abort, Flask, jsonify, redirect, render_template, request, session, url_for
from flask.ext.cors import cross_origin
from flask.ext.sqlalchemy import SQLAlchemy

from consts import SECRET_KEY, ISO_CODE_TO_COUNTRY_NAME, STRINGS_D, STORIES, SURVEYS, QUESTIONS

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
	return render_template("splash.html")

@app.route("/set_lang/", methods=["POST"])
def set_lang():
	if "lang" not in request.form or (request.form["lang"] != "en" and request.form["lang"] != "chn"):
		abort(403)
	session["lang"] = request.form["lang"]
	return redirect(url_for("get_consent"))

@app.route("/consent/", methods=["GET"])
def get_consent():
	if "lang" not in session:
		return redirect(url_for("main"))
	return render_template("consent.html", lang=session["lang"],
										   strings_d=STRINGS_D)

@app.route("/set_consent/", methods=["POST"])
def set_consent():
	if "lang" not in session or "consent" not in request.form or (request.form["consent"] != "agree" and request.form["consent"] != "disagree"):
		abort(403)
	if request.form["consent"] == "agree":
		session["consent"] = True
		return redirect(url_for("get_demographics"))
	else:
		session["consent"] = False
		return redirect(url_for("no_consent"))

@app.route("/get_demographics", methods=["GET"])
def get_demographics():
	if "lang" not in session:
		return redirect(url_for("main"))
	elif "consent" not in session:
		return redirect(url_for("get_demographics"))
	elif session["consent"] == False:
		return redirect(url_for("no_consent"))
	return render_template("demographics.html", lang=session["lang"],
												strings_d=STRINGS_D)

@app.route('/set_demographics/', methods=['POST'])
def set_demographics():
	if "lang" not in session or "consent" not in session or !session["consent"]:
		abort(403)
	if ('age' not in request.form or 'gender' not in request.form
		or 'education' not in request.form or 'country_origin' not in request.form
		or 'country_residence' not in request.form or 'native_lang' not in request.form):
		abort(403)
	session['age'] = request.form['age']
	session['gender'] = request.form['gender']
	session['education'] = request.form['education']
	session['country_origin'] = request.form['country_origin']
	session['country_residence'] = request.form['country_residence']
	session['native_lang'] = request.form['native_lang']
	session['demographics_complete'] = True
	survey_data = get_survey_data()
	try:
		return render_template('survey.html', survey_data=survey_data,
										  	  code_to_name=ISO_CODE_TO_COUNTRY_NAME,
										  	  lang=session['lang'],
										  	  strings_d=STRINGS_D)
	except:
		print 'Unexpected error:'
		traceback.print_exc()

# @app.route('/handle_survey', methods=['POST'])
# def handle_survey():
# 	if ('demographics_complete' not in session or 'survey_submitted' in session): abort(403)
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
# 		if len(question_ids) >= 23:
# 			survey.q22 = int(question_ids[22])
# 			survey.q22_ans = form_data[question_ids[22]]
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

# @app.route('/validate_survey_completion', methods=['POST'])
# @cross_origin()
# def validate_survey_completion():
# 	data = request.get_json()
# 	if 'confirmation_code' not in data:
# 		return jsonify({'success': False})
# 	confirmation_code = data['confirmation_code']
# 	confirmation_code_split = confirmation_code.split(';')
# 	if len(confirmation_code_split) == 2:
# 		identifier, code = confirmation_code_split
# 		query_result = (db.session.query(Survey).filter(Survey.id == identifier)).first()
# 		if query_result and query_result.confirmation_code == code and not query_result.confirmed:
# 			query_result.confirmed = True
# 			db.session.commit()
# 			return jsonify({'success': True, 'confirmation_code': confirmation_code})
# 		else:
# 			return jsonify({'success': False})
# 	else:
# 		return jsonify({'success': False})

def get_survey_data():
	"""
	Returns a dict whose data characterizes a new survey instance.
	Such data exactly includes:
	- the order of 
	- 
	- 
	- 
	"""
	survey_question_ids = list(SURVEYS[survey_num])
	random.shuffle(survey_question_ids)
	survey_question_ids.insert(6, 645)
	survey_question_ids.insert(15, 646)
	survey_data = []
	for question_id in survey_question_ids:
		survey_datum = {}
		survey_question_data = dict(QUESTIONS[question_id])

		survey_datum['question_id'] = question_id
		survey_question_answer_choices = list(survey_question_data['choices'])
		random.shuffle(survey_question_answer_choices)
		survey_datum['answer_choices'] = survey_question_answer_choices
		if session['lang'] == 'en':
			survey_question_story = STORIES[survey_question_data['story_id']]['english_rewrite']
		else:
			survey_question_story = (STORIES[survey_question_data['story_id']]['chinese_rewrite']).decode('UTF-8')
		survey_datum['story'] = survey_question_story

		survey_data.append(survey_datum)
	return survey_data

if __name__ == '__main__':
	app.run(debug=True)
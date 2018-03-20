from flask import Flask, render_template, redirect, url_for, request
import pymysql
app = Flask(__name__)
app.static_folder='static'

@app.route("/Index")
def Index():
	return render_template('Index.html')

@app.route("/Menu")
def Menu():
	return render_template('Menu.html')

@app.route("/AboutUs")
def AboutUS():
	return render_template('AboutUs.html')

@app.route("/AboutUsSent", methods=['POST','GET']) #insert comment into database
def AboutUsSent():
	if request.method=='POST':
		UserComment=request.form.get("comment")
		db=pymysql.connect("localhost","root","04051998","205")
		cursor=db.cursor()
		try:
			cursor.execute("""INSERT INTO `comment`(`usercomment`) VALUES ('%s')""" %UserComment)	
			db.commit()
		except:
			db.rollback()	

		return render_template('AboutUs.html')
		db.close()

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/signup")
def signup():
	return render_template('signup.html')

@app.route("/login/<usrname>") #loginpage
def user_page( usrname):
	db=pymysql.connect("localhost","root","04051998","205")
	cursor=db.cursor()
	cursor.execute("SELECT `id` FROM `user`WHERE username='%s'"%usrname)
	catchname=cursor.fetchall()
	for row in catchname:
		userid=row[0]
		cursor.execute("SELECT `points` FROM `card`WHERE id='%s'"%userid)
		points=cursor.fetchall()
		for row in points:
			point = row[0]
		return render_template('loginpage.html',name=usrname,point=point)
	db.close()

@app.route("/result", methods=['POST','GET']) #login.html
def result():
	db=pymysql.connect("localhost","root","04051998","205")
	cursor=db.cursor()
	cursor.execute("SELECT `username`,`password` FROM `user`")
	result=cursor.fetchall()
	if request.method == 'POST':
		userName=request.form.get("username")
		userPassword=request.form.get("password")
		for row in result:
			if userName==row[0] and userPassword!=row[1]:
				return render_template('login.html',wrong="The Password is not correct!")
			elif userName==row[0] and userPassword==row[1]:
				return redirect(url_for('user_page',usrname=userName))
				break
		else:
			return render_template('login.html',wrong="The information is not correct!")
		db.close()


@app.route("/ok", methods=['POST','GET']) #signup.html
def ok():
	db=pymysql.connect("localhost","root","04051998","205")
	cursor=db.cursor()
	cursor.execute("SELECT `username` FROM `user`")
	memberID=cursor.fetchall()
	if request.method == 'POST':
		InputName=request.form.get("username")
		InputPassword=request.form.get("password")
		InputEmail=request.form.get("email")
		MemberNumber=request.form.get("membercardid")
		ConfirmPassword=request.form.get("confirm_password")
		for row in memberID:
			if InputPassword!=ConfirmPassword:
				return render_template('signup.html',error="The Confirm Password is not same as your Password! Please try again!")
			elif InputName==row[0]:
				return render_template('signup.html',error="The Username has been used! Please enter another Username!")			
			else:
				try:
					cursor.execute("""INSERT INTO `user`(`username`,`password`,`email`,`id`) VALUES ('%s','%s','%s','%s')""" %(InputName,InputPassword,InputEmail,MemberNumber))	
					db.commit()
				except:
					db.rollback()	

				return render_template('login.html',ok="You can login now!")
				db.close()



if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0", port=8000)
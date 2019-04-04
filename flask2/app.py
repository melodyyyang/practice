from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

	if request.method == "POST":
		#retrieve login details
		username = request.form["username"]
		password = request.form["password"]

		print(username, password)
		#check if username exists, and password is correct

		#login the user

		return redirect(url_for("index"))
	return render_template("login.html")

app.run(debug=True)
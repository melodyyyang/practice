from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def index():
	
	return render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
def home():
	
	return "This is my home page"


@app.route("/names")
def names():
	
	return render_template("names.html")

@app.route("/home/<name>")
def home_name(name):

	x = ["melody", "althea", "lay"]

	number = 12

	return render_template("home.html", variable_name = x, y = number)



app.run(debug=True) 
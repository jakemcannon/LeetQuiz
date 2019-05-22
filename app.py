from flask import Flask, render_template, jsonify

app = Flask(__name__)


posts = [
	{
		'author': 'Jake Cannon',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date_posted': 'November 19, 2019'
	},
	{
		'author': 'Tyler Cannon',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': 'November 19, 2019'
	}
]



@app.route("/")
@app.route("/home")
def hello():
	return render_template('home.html', posts=posts)

@app.route("/api/v1/resources/books/all", methods=['GET'])
def api_all():
	return jsonify(posts)


@app.route("/about")
def about():
	return render_template('about.html')



if __name__ == '__main__':
	app.run(debug=True)
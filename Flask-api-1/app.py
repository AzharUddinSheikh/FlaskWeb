from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'robin',
        'title': 'blog post1',
        'content': 'first post content',
        'date': 'april 20 2019'
    },
    {
        'author': 'jack kallis',
        'title': 'blog sample',
        'content': 'second content',
        'date': 'march 20 2009'
    }
]


@app.route('/')
def home():
    return "<h1>Home</h1>"


@app.route('/about')
def about():
    return render_template('about.html', posts=posts)
    # our posts which is above list variable and which gone into templates


if __name__ == "__main__":
    app.run(debug=True)

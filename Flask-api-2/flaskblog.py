from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Azhar',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'December 28,2020'
    },
    {
        'author': 'Ajju',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'December 29,2020'
    }
]


@app.route('/')
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


if __name__ == "__main__":
    app.run(debug=True)

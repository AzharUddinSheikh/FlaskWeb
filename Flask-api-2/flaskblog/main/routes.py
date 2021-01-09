from flask import request, render_template, Blueprint
from flaskblog.models import Posts

main = Blueprint('main',__name__)


@main.route('/')
def home():
    #  taking page query argument 1 is default type is integer or error throw
    page = request.args.get('page',1,type=int)
    # making our post in desc order sequence 
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page,per_page=2)
    #  per page only 2 post and page is an arg of posts
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About Page')

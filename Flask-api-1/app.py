from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'aazhar'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accout Created for {form.username.data}!', 'success')

        return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


if __name__ == "__main__":
    app.run(debug=True)

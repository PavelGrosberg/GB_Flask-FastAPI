from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/welcome/')
def welcome():
    name = request.form['name']
    email = request.form['email']

    response = make_response(redirect(url_for('welcome_page')))
    response.set_cookie('user_data', f'{name},{email}')

    return response


@app.route('/welcome_page')
def welcome_page():
    user_data = request.cookies.get('user_data', None)

    if user_data:
        name, email = user_data.split(',')
        return render_template('welcome.html', name=name, email=email)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_data')
    return response


if __name__ == '__main__':
    app.run(debug=True)

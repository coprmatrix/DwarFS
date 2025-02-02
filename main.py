
from flask import Flask, redirect, session, request, render_template_string
from flask_openid import OpenID
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random key
oid = OpenID(app, '/tmp/openid_cache')

@app.route('/')
def index():
    if 'openid' in session:
        return f'''
            <h1>Welcome!</h1>
            <p>You are logged in as: {session['openid']}</p>
            <a href="/logout">Logout</a>
        '''
    return '''
        <h1>Welcome!</h1>
        <form method="post" action="/login_fedorainfracloud">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit">Login with Fedora OpenID</button>
        </form>
    '''

@app.route('/login_fedorainfracloud', methods=['POST'])
def login_fedorainfracloud():
    csrf_token = request.form.get('csrf_token')
    # Verify the CSRF token if needed.
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if request.method == 'POST':
        return oid.try_login(request.form['openid'], ask_for=['nickname', 'email'])

    return oid.try_login('https://id.fedoraproject.org/openid', ask_for=['nickname', 'email', 'yahoo'])

@app.route('/logout')
def logout():
    session.pop('openid', None)
    return redirect('/')

@oid.after_login
def after_login(resp):
    session['openid'] = resp.identity_url  # Store OpenID identity URL
    print(resp.__dict__)
    print(oid.__dict__)
    print(oid.store_factory.__dict__)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



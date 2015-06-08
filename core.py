"""
Server Core
"""

from flask import Flask, jsonify, render_template, request
import random
import time
from string import ascii_lowercase
from hashlib import md5

app = Flask(__name__,  static_url_path='')
max_passwords_amount = 10
allowed_symbols = [str(digit) for digit in range(10)] + [alpha for alpha in ascii_lowercase]
sent_hashes = []
UsersOnline = 0
start_time = 0


def generate_password(n):
    """Generates random password from server-defined symbols."""
    assert n > 0
    res = ''
    for i in range(n):
        res += allowed_symbols[random.randint(0, len(allowed_symbols) - 1)]
    return res


@app.route('/calculate_current')
def calculate():
    """Return current data for calculation(hash)."""
    print ':::GET FIRST:::  Request to get hash and begin to brut password'
    global allowed_symbols, sent_hashes, max_passwords_amount, start_time
    if len(sent_hashes) <= max_passwords_amount:
        start_time = time.time()
        gen_pwd = generate_password(4)
        gen_hash = md5(gen_pwd).hexdigest()
        sent_hashes.append(gen_hash)
        print ':::SENT:::       Hash "{0}" of "{1}" password sent'.format(gen_hash, gen_pwd)
    else:
        print ':::SENT:::       Nothing to send to the new client. All passwords are sent!'
        gen_hash = ''
    return jsonify(hash=gen_hash)


@app.route('/online')
def online():
    """Returns number of online clients."""
    global UsersOnline
    print ':::GET USERS:::      request to get online user count; users online now: ', UsersOnline
    return jsonify(result=UsersOnline)


@app.route('/users_online')
def users_online():
    """Renders page, that displaying number of online clients."""
    return render_template('online.html')


@app.route('/watch_worker', methods=['POST'])
def watch_worker():
    """Watch current worker state."""
    global allowed_symbols, sent_hashes, max_passwords_amount, start_time
    received_data = request.json
    if received_data == 0:
        if len(sent_hashes) <= max_passwords_amount:
            print ':::WORKING:::    working for {0} seconds: '.format(time.time() - start_time)
        else:
            print ':::FINISH:::     Nothing to sent!'
            gen_hash = ''
    else:
        print ':::RESULT:::     hash "{0}" computed on worker in {1} seconds: '.format(sent_hashes[0], time.time() - start_time)
        print ':::RESULT:::     The resulting password is: "{0}"'.format(received_data)
        if len(sent_hashes) <= max_passwords_amount:
            start_time = time.time()
            gen_pwd = generate_password(4)
            gen_hash = md5(gen_pwd).hexdigest()
            sent_hashes.append(gen_hash)
            print ':::SENT:::       Next hash "{0}" of "{1}" password sent to worker'.format(gen_hash, gen_pwd)
        else:
            print ':::SENT:::       Nothing to send to the current worker. All passwords are sent!'
            gen_hash = ''
    return jsonify(hash=gen_hash)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders main page. Case work is finished returns alert message."""
    global max_passwords_amount, sent_hashes
    if len(sent_hashes) >= max_passwords_amount:
        return render_template('finish.html')
    return render_template('index.html')


@app.route('/mark_online', methods=['POST'])
def mark_online():
    """Marks client online."""
    user_id = request.remote_addr
    # mark user, before worker started
    global UsersOnline
    UsersOnline += 1
    print ':::NEW CLIENT::: client registered: ', user_id
    return jsonify(result=user_id)


@app.route('/mark_offline', methods=['POST'])
def mark_offline():
    """Marks client offline."""
    user_id = request.remote_addr
    global UsersOnline
    if UsersOnline != 0:
        UsersOnline -= 1
        print ':::CLIENT DISCONNECT::: client gone offline: ', user_id
    return jsonify(result=user_id)


if __name__ == "__main__":
    app.run(host='127.0.0.1')  # making server visible across local network for test purposes

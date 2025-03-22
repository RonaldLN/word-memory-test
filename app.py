from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pathlib import Path
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret')
PASSWORD = os.getenv('APP_PASSWORD', 'default-password')

# 添加应用前缀中间件
class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        return self.app(environ, start_response)
    
app.wsgi_app = ReverseProxied(app.wsgi_app)

class WordMemoryTest:
    def __init__(self, word_list, history_file='history.json'):
        self.word_list = word_list
        self.history_file = Path(history_file)
        self.history = self._load_history()
        self.last_word = None

    def _load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f) or {}
        return {}

    def _save_history(self):
        temp_file = self.history_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(self.history, f, indent=4)
        temp_file.replace(self.history_file)

    def _update_history(self, word, remembered):
        if word not in self.history:
            self.history[word] = [0, 0]
        self.history[word][0] += 1
        if not remembered:
            self.history[word][1] += 1

    def _get_weights(self):
        candidates = [w for w in self.word_list if w != self.last_word]
        return [self.history.get(w, [0,0])[1] + 1 for w in candidates]

    def get_next_word(self):
        candidates = [w for w in self.word_list if w != self.last_word]
        if not candidates:
            candidates = self.word_list
        weights = self._get_weights()
        chosen = random.choices(candidates, weights=weights, k=1)[0]
        self.last_word = chosen
        return chosen

def load_words_from_json():
    if Path('history.json').exists():
        with open('history.json', 'r') as f:
            return list(json.load(f).keys())
    return []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            session.pop('last_word', None)
            return redirect(url_for('index'))
        return "密码错误", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('last_word', None)
    # 使用url_for确保重定向路径正确
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/next', methods=['POST'])
def next_word():
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    current_word = data.get('current_word')
    remembered = data.get('remembered', False)
    
    word_list = load_words_from_json()
    test = WordMemoryTest(word_list)
    
    # 更新历史记录
    if current_word:
        test.last_word = current_word
        test._update_history(current_word, remembered)
        test._save_history()
    
    # 获取新单词
    new_word = test.get_next_word()
    session['last_word'] = new_word
    
    return jsonify({'word': new_word})

if __name__ == '__main__':
    app.run(debug=True)
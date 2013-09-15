from flask import Flask, url_for, redirect, request, render_template
import sys
sys.path.insert(0, 'sentGen')
from generator import get_all_data, generate, generate_multiple
app = Flask(__name__)

sys.path.insert (0, 'Predictor')
from predictor2 import train, set_priors, predictor_func, run_tests, get_text
from predictor_helper import test

@app.route('/')
def main_page():
    return render_template('login.html')

@app.route('/hashtag/<button>', methods=['POST', 'GET'])
def hashtag(button):
    if request.method=='POST':
	if button == "1":
	    hashtag = request.form['hashtag']
	    return render_template('hashtag.html', sentence= generate (hashtag), cleanhashtag = hashtag[1:])
	else:
	    assert (button == "2")
	    text = request.form ['text']
	    #print text
	    #print text.split ()
	    result = test (text.split(), predictor_func)
	    #print result
	    htag_text = get_text (result).decode ("ascii")
	    #print htag_text
	    return render_template('hashtaglist.html', sentence=text, hashtag_text = htag_text)

    else:
        return 'You messed up'

app.debug = False
if __name__ == '__main__':
    app.run(debug=True)

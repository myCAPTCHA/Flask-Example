"""
 * This code was created by myCaptcha.
 * myCAPTCHA is a free captcha service that allows you to protect your site with a captcha with no charge.
 *
 * Licensed under the MIT License. You may obtain a copy of the License at
 * https://opensource.org/licenses/MIT
 *
 * @author myCaptcha
 * @license MIT
 * @link https://www.mycaptcha.org
"""

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.mycaptcha.org"
API_KEY = "API_KEY"

def get_captcha(api_key):
    response = requests.get(f"{API_BASE_URL}/captcha", params={'api_key': api_key})
    if response.status_code == 200:
        return response.json()
    return None

def validate_captcha(code, answer):
    data = {"code": code, "answer": answer}
    response = requests.post(f"{API_BASE_URL}/validate_captcha", json=data)
    if response.status_code == 200:
        return response.json().get("valid", False)
    return False

@app.route('/', methods=['GET'])
def index():
    global API_KEY

    captcha = get_captcha(API_KEY)
    if captcha:
        captcha_image = captcha["url"]
        captcha_code = captcha["code"]
        return render_template_string('''
          <form action="/verify" method="post">
            <p>Please solve the following captcha:</p>
            <img src="{{captcha_image}}" alt="Captcha"/>
            <input type="hidden" name="captcha_code" value="{{captcha_code}}"/>
            <input name="answer" required />
            <button type="submit">Submit</button>
          </form>
        ''', captcha_image=captcha_image, captcha_code=captcha_code)
    return "Failed to load captcha. Please try again."

@app.route('/verify', methods=['POST'])
def verify():
    captcha_code = request.form['captcha_code']
    answer = request.form['answer']
    if validate_captcha(captcha_code, answer):
        return "Captcha validation successful."
    else:
        return "<script>location.replace('/');</script>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

import os
from flask_uploads import UploadSet, configure_uploads, DATA
from flask import Flask, render_template, jsonify, request, url_for
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        request_form = data = request.form.to_dict()
        print("\nFORM: ", request_form, "\n")
    return render_template('Blog Template.html')

if __name__ == "__main__":
    # the main function just runs the app
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT, debug = True) #savethis

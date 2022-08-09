from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, request, send_file

# Flask app instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/videos'

@app.route('/')
def index():
    return render_template('index.html', files=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        video = request.files['upload']
        print(video)
        file_name, file_extention = os.path.splitext(video.filename)
        final_file_name = f"video_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}{file_extention}"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], final_file_name)
        video.save(video_path)
    return redirect(url_for('index'))

@app.route('/download', methods=['GET'])
def download():
    video = request.args.get('file')
    video_path = "static/videos" + "/" + video
    return send_file(video_path, as_attachment=True)

@app.route('/reset', methods=['GET'])
def reset():
    dir = app.config['UPLOAD_FOLDER']
    for f in os.listdir(dir):
        if not f == 'readme.txt':
            os.remove(os.path.join(dir, f))
    return redirect(url_for('index'))
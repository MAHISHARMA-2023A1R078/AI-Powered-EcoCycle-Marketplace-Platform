from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'Mahi_Sharma')
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    return render_template('dashboard.html', username=username, database_images=images)

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    label = request.form.get('ai_label')
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    sugg = f"EcoCycle identifies this as {label}. "
    if "Reuse" in label: sugg += "Perfect for a creative DIY project!"
    else: sugg += "Dispose in the green bin for local recycling."

    return jsonify({"reason": sugg, "status": "success"})

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
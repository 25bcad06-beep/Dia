from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('aarya.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    print(f"{name} ({email}) says: {message}")

    return jsonify({"message": "Message sent successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
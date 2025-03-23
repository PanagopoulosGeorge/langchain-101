# /c:/Users/George/Desktop/projects/Thesis/project/langchain-101/app.py
from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break_with

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    summary, profile_pic_url = ice_break_with(name=text)
    return jsonify(
                {"summary": summary, 
                 "profile_pic_url": profile_pic_url}
    )

if __name__ == "__main__":
    app.run(debug=True)
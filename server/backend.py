from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/screen", methods=["POST"])
def submitScreen():
    requestBody = request.json()
    print(requestBody)
    

if __name__=="__main__":
    app.run(debug=True)
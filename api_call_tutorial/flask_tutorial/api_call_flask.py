from flask import Flask,jsonify
app=Flask(__name__)
print(__name__)

@app.route("/api",methods=["GET"])
def api_example():
    response={
        "message":"Hello from FLASK API"
    }
    return jsonify(response)

if __name__=="__main__":
    app.run(debug=True)
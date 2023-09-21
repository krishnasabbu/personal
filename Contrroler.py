import joblib
from flask import Flask, request, jsonify


app = Flask(__name__)

cdqa_pipeline=joblib.load('./models/bert_wells.joblib')

@app.route("/chat", methods=["GET"])
def chat():
    query = request.args.get("q")
    prediction = cdqa_pipeline.predict(query=query)
    return jsonify(
        query=query, answer=prediction[0], title=prediction[1], paragraph=prediction[2]
    )
    
app.run()

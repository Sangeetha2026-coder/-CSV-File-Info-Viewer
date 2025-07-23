from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=['GET'])
def Home():
    return render_template("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files["file"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)


    df = pd.read_csv(filepath)
    rows, cols = df.shape
    null_values = df.isnull().sum().to_dict()
    total_nulls = sum(null_values.values())
    summary = df.describe().T.to_dict(orient='index')



  
    return render_template('result.html',
                           data=[rows, cols],
                           total_nulls=total_nulls,
                           desc=summary,)


@app.route("/export_json", methods=["POST"])
def export_json():
    csv_file = r"C:\Users\DELL\Documents\Sangeetha\Python\project\Data Exploration & Preprocessing\csv file into viewer\uploads\sample_data.csv"
    json_file = r"C:\Users\DELL\Documents\Sangeetha\Python\project\Data Exploration & Preprocessing\csv file into viewer\uploads\sample_data.json"

    try:
        df = pd.read_csv(csv_file)  
        df=df.fillna(0)                  
        records = df.to_dict(orient="records") 
        wrapped_data = {"data": records}
        
        
        with open(json_file, "w") as f:
            json.dump(wrapped_data, f, indent=4)

        
        return send_file(json_file, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

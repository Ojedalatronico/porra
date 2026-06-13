from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_PATH = os.path.join("data", "resultados_porra.csv")

def get_df():
    if not os.path.exists(CSV_PATH):
        return None
    return pd.read_csv(CSV_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/leaderboard")
def leaderboard():
    df = get_df()
    if df is None:
        return jsonify([])
    # Group by participant and sum points
    leaderboard_df = df.groupby("Participante")["Puntos"].sum().reset_index()
    leaderboard_df = leaderboard_df.sort_values(by="Puntos", ascending=False)
    return jsonify(leaderboard_df.to_dict(orient="records"))

@app.route("/api/participants")
def participants():
    df = get_df()
    if df is None:
        return jsonify([])
    return jsonify(sorted(df["Participante"].unique().tolist()))

@app.route("/api/user_results/<name>")
def user_results(name):
    df = get_df()
    if df is None:
        return jsonify([])
    user_data = df[df["Participante"] == name]
    # Convert NaN to None for JSON
    user_data = user_data.replace({pd.NA: None, float('nan'): None})
    return jsonify(user_data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

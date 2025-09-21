from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Path to leaderboard CSV (update as needed)
LEADERBOARD_CSV = os.path.join(os.path.dirname(__file__), '../v2_leaderboard_20250921_154909.csv')

@app.route('/')
def index():
    # Load leaderboard data
    df = pd.read_csv(LEADERBOARD_CSV)
    columns = df.columns.tolist()
    # The model column in this file is 'Model'
    models = sorted(df['Model'].unique()) if 'Model' in df else []
    # Filtering by model if requested
    selected_model = request.args.get('model', '')
    if selected_model:
        df = df[df['Model'] == selected_model]
    return render_template('index.html', tables=[df.to_html(classes='table table-striped', index=False)], columns=columns, models=models, selected_model=selected_model)

if __name__ == '__main__':
    app.run(debug=True)

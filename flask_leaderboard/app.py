#!/usr/bin/env python3
"""
Enhanced Flask Leaderboard for HumanEvalComm V2 Benchmark

Features:
- Auto-detects latest leaderboard files
- Interactive charts and visualizations
- Multiple filtering and sorting options
- Real-time data refresh
- Responsive design with modern UI
- Robust error handling
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import json
import os
import glob
from datetime import datetime
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)

class LeaderboardManager:
    """Manages leaderboard data and operations."""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.cache = {}
        self.cache_time = {}
        
    def find_latest_files(self):
        """Find the latest leaderboard and results files."""
        # Look for V2 leaderboard files
        leaderboard_pattern = os.path.join(self.base_dir, 'v2_*leaderboard*.csv')
        results_pattern = os.path.join(self.base_dir, 'v2_*results*.json')
        
        leaderboard_files = glob.glob(leaderboard_pattern)
        results_files = glob.glob(results_pattern)
        
        # Sort by modification time (newest first)
        leaderboard_files.sort(key=os.path.getmtime, reverse=True)
        results_files.sort(key=os.path.getmtime, reverse=True)
        
        return {
            'leaderboard_files': leaderboard_files,
            'results_files': results_files,
            'latest_leaderboard': leaderboard_files[0] if leaderboard_files else None,
            'latest_results': results_files[0] if results_files else None
        }
    
    def load_leaderboard_data(self, file_path=None):
        """Load leaderboard data with caching."""
        if file_path is None:
            files = self.find_latest_files()
            file_path = files['latest_leaderboard']
            
        if not file_path or not os.path.exists(file_path):
            return None
            
        # Check cache
        cache_key = f"leaderboard_{file_path}"
        file_mtime = os.path.getmtime(file_path)
        
        if cache_key in self.cache and self.cache_time.get(cache_key, 0) >= file_mtime:
            return self.cache[cache_key]
        
        try:
            df = pd.read_csv(file_path)
            
            # Clean and process data with robust error handling
            for col in df.columns:
                if col == 'Model':
                    continue  # Skip model column
                    
                # Convert all data columns to string first for cleaning
                df[col] = df[col].astype(str)
                
                # Clean malformed data like '100%100%' or '50%'
                if df[col].str.contains('%').any():
                    # Remove all % signs and extract first number
                    df[col] = df[col].str.replace('%', '', regex=False)
                    # Extract first number if there are multiple concatenated
                    df[col] = df[col].str.extract(r'(\d+(?:\.\d+)?)', expand=False)
                
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Debug: print cleaned DataFrame info
            print(f"[DEBUG] Successfully loaded and cleaned {file_path}")
            print(f"[DEBUG] DataFrame shape: {df.shape}")
            print(f"[DEBUG] Columns: {df.columns.tolist()}")
            
            # Cache the data
            self.cache[cache_key] = df
            self.cache_time[cache_key] = file_mtime
            
            return df
            
        except Exception as e:
            print(f"Error loading leaderboard data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_detailed_results(self, file_path=None):
        """Load detailed results data."""
        if file_path is None:
            files = self.find_latest_files()
            file_path = files['latest_results']
            
        if not file_path or not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading results data: {e}")
            return None
    
    def get_summary_stats(self, df):
        """Get summary statistics."""
        if df is None or df.empty:
            return {}
            
        stats = {
            'total_models': len(df),
            'avg_v2_score': df['V2 Score'].mean() if 'V2 Score' in df else 0,
            'avg_comm_rate': df['Comm Rate'].mean() if 'Comm Rate' in df else 0,
            'avg_pass_at_1': df['Pass@1'].mean() if 'Pass@1' in df else 0,
            'top_model': df.iloc[0]['Model'] if not df.empty else 'N/A',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return stats

# Initialize manager
manager = LeaderboardManager()

@app.route('/')
def index():
    """Main leaderboard page."""
    try:
        # Load data
        df = manager.load_leaderboard_data()
        files_info = manager.find_latest_files()
        
        if df is None:
            return render_template('error.html', 
                                 error="No leaderboard data found. Please run the V2 benchmark first.")
        
        # Get filtering parameters
        selected_model = request.args.get('model', '')
        sort_by = request.args.get('sort_by', 'V2 Score')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Apply filters
        filtered_df = df.copy()
        if selected_model:
            filtered_df = filtered_df[filtered_df['Model'] == selected_model]
        
        # Apply sorting
        if sort_by in filtered_df.columns:
            ascending = sort_order == 'asc'
            filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
        
        # Get summary stats
        stats = manager.get_summary_stats(filtered_df)
        
        # Get available models and columns
        models = sorted(df['Model'].unique()) if 'Model' in df else []
        columns = [col for col in df.columns if col != 'Model']
        
        return render_template('index.html',
                             df=filtered_df,
                             models=models,
                             columns=columns,
                             selected_model=selected_model,
                             sort_by=sort_by,
                             sort_order=sort_order,
                             stats=stats,
                             files_info=files_info)
                             
    except Exception as e:
        return render_template('error.html', error=f"Error loading leaderboard: {e}")

@app.route('/api/data')
def api_data():
    """API endpoint for leaderboard data."""
    try:
        df = manager.load_leaderboard_data()
        if df is None:
            return jsonify({'error': 'No data available'})
        
        return jsonify({
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'models': sorted(df['Model'].unique()) if 'Model' in df else [],
            'stats': manager.get_summary_stats(df)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/charts')
def api_charts():
    """API endpoint for chart data."""
    try:
        df = manager.load_leaderboard_data()
        if df is None:
            return jsonify({'error': 'No data available'})
        
        # Create chart data
        # Prepare chart containers (always include keys to avoid missing-key issues on the frontend)
        charts = {
            'v2_scores': {'x': [], 'y': []},
            'communication': {'models': [], 'comm_rate': [], 'good_q_rate': []},
            'performance_radar': {'models': [], 'metrics': [], 'values': []},
            'trustworthiness': {},
            'heatmap': {'x': [], 'y': [], 'z': []}
        }

        # V2 Score comparison
        if 'V2 Score' in df.columns:
            charts['v2_scores'] = {
                'x': df['Model'].tolist(),
                'y': df['V2 Score'].tolist()
            }

        # Communication metrics
        if 'Comm Rate' in df.columns and 'Good Q Rate' in df.columns:
            charts['communication'] = {
                'models': df['Model'].tolist(),
                'comm_rate': df['Comm Rate'].tolist(),
                'good_q_rate': df['Good Q Rate'].tolist()
            }
        
        # Performance radar & trustworthiness metrics
        performance_cols = ['Pass@1', 'Test Pass', 'Readability', 'Security', 'Efficiency', 'Reliability']
        available_perf_cols = [col for col in performance_cols if col in df.columns]

        if available_perf_cols:
            # Build a radar-friendly structure: metrics list and values per model
            models = df['Model'].tolist()
            metrics = available_perf_cols
            # values: list of lists, each inner list contains metric values for one model (in same order as metrics)
            values = []
            for _, row in df.iterrows():
                values.append([row[col] for col in metrics])

            charts['performance_radar'] = {
                'models': models,
                'metrics': metrics,
                'values': values
            }

        # Trustworthiness grouping (explicit metrics expected by the frontend)
        trust_metrics = ['Readability', 'Security', 'Efficiency', 'Reliability']
        available_trust = [m for m in trust_metrics if m in df.columns]
        if available_trust:
            trust = {'models': df['Model'].tolist()}
            for m in available_trust:
                trust[m] = df[m].tolist()
            charts['trustworthiness'] = trust
        else:
            # Ensure trustworthiness has an explicit models key for frontend sanity
            charts['trustworthiness'] = {'models': []}

        # Heatmap: rows = models, cols = selected metrics (use performance metrics if available)
        if available_perf_cols:
            heatmap_z = []
            heatmap_x = available_perf_cols
            heatmap_y = df['Model'].tolist()
            for _, row in df.iterrows():
                heatmap_z.append([row[col] for col in heatmap_x])

            charts['heatmap'] = {
                'x': heatmap_x,
                'y': heatmap_y,
                'z': heatmap_z
            }

        # Debug: print quick summary to server logs for easier diagnosis
        try:
            print('[DEBUG] /api/charts: v2_scores:', len(charts.get('v2_scores', {}).get('x', [])),
                  'communication:', len(charts.get('communication', {}).get('models', [])),
                  'performance_radar_models:', len(charts.get('performance_radar', {}).get('models', [])),
                  'trust_models:', len(charts.get('trustworthiness', {}).get('models', [])),
                  'heatmap_rows:', len(charts.get('heatmap', {}).get('y', [])))
        except Exception:
            pass
        
        return jsonify(charts)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/detailed')
def detailed():
    """Detailed results page."""
    try:
        results_data = manager.load_detailed_results()
        files_info = manager.find_latest_files()
        
        if results_data is None:
            return render_template('error.html', 
                                 error="No detailed results found. Please run the V2 benchmark first.")
        
        # Process results for display
        df_results = pd.DataFrame(results_data)
        
        # Get filtering parameters
        selected_model = request.args.get('model', '')
        selected_problem = request.args.get('problem', '')
        
        # Apply filters
        if selected_model:
            df_results = df_results[df_results['model_name'] == selected_model]
        if selected_problem:
            df_results = df_results[df_results['problem_id'] == selected_problem]
        
        # Get available options
        models = sorted(df_results['model_name'].unique()) if 'model_name' in df_results else []
        problems = sorted(df_results['problem_id'].unique()) if 'problem_id' in df_results else []
        
        # Load problems data for question display
        problems_data = {}
        try:
            # Try to load from HumanEvalComm_v2.jsonl
            problems_file = os.path.join(manager.base_dir, 'Benchmark',
                                         'HumanEvalComm_v2.jsonl')
            if os.path.exists(problems_file):
                problems_data = {}
                with open(problems_file, 'r') as f:
                    for line in f:
                        problem = json.loads(line.strip())
                        problem_id = problem.get('name', '')
                        if problem_id:
                            # Use the appropriate prompt based on prompt_type
                            prompt = problem.get('prompt', '')
                            problems_data[problem_id] = {
                                'prompt': prompt,
                                'entry_point': problem.get('entry_point', ''),
                                'test_case': problem.get('test_case', [])
                            }
        except Exception as e:
            print(f"Warning: Could not load problems data: {e}")
        
        # Format last updated timestamp
        last_updated = 'N/A'
        if (files_info.get('latest_results') and
                os.path.exists(files_info['latest_results'])):
            try:
                mtime = os.path.getmtime(files_info['latest_results'])
                last_updated = datetime.fromtimestamp(mtime).strftime(
                    '%Y-%m-%d %H:%M')
            except Exception:
                pass

        return render_template('detailed.html',
                               df=df_results,
                               models=models,
                               problems=problems,
                               selected_model=selected_model,
                               selected_problem=selected_problem,
                               files_info=files_info,
                               last_updated=last_updated,
                               problems_data=problems_data)

    except Exception as e:
        error_msg = f"Error loading detailed results: {e}"
        return render_template('error.html', error=error_msg)


@app.route('/refresh')
def refresh():
    """Refresh data cache."""
    try:
        manager.cache.clear()
        manager.cache_time.clear()
        return jsonify({'status': 'success', 'message': 'Cache refreshed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/files')
def files():
    """List available files."""
    try:
        files_info = manager.find_latest_files()
        return jsonify(files_info)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

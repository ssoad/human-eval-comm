"""
Evaluation Dashboard

Simple web dashboard for visualizing evaluation results and model performance.
Provides interactive charts and leaderboards for different evaluation dimensions.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class EvaluationDashboard:
    """Dashboard for visualizing evaluation results."""

    def __init__(self, results_dir: str = "results"):
        """Initialize the dashboard."""
        self.results_dir = results_dir
        self.results_data = []
        os.makedirs(results_dir, exist_ok=True)

    def load_results(self, results_file: str = "evaluation_results.jsonl"):
        """Load evaluation results from file."""
        results_path = os.path.join(self.results_dir, results_file)

        if not os.path.exists(results_path):
            logger.warning(f"Results file not found: {results_path}")
            return

        try:
            with open(results_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            result = json.loads(line)
                            self.results_data.append(result)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Skipping malformed JSON at line {line_num}: {e}")
                        except Exception as e:
                            logger.warning(f"Skipping problematic result at line {line_num}: {e}")

            logger.info(f"Loaded {len(self.results_data)} evaluation results")

        except Exception as e:
            logger.error(f"Failed to load results file: {e}")

    def generate_leaderboard(self, metric: str = "standard_composite_score") -> List[Dict[str, Any]]:
        """Generate leaderboard sorted by specified metric."""
        if not self.results_data:
            return []

        # Group by model and calculate averages
        model_stats = {}

        for result in self.results_data:
            model_name = result.get('model_name', 'unknown')
            score = result.get(metric, 0)

            if model_name not in model_stats:
                model_stats[model_name] = {
                    'model_name': model_name,
                    'scores': [],
                    'count': 0
                }

            model_stats[model_name]['scores'].append(score)
            model_stats[model_name]['count'] += 1

        # Calculate averages and sort
        leaderboard = []
        for model_name, stats in model_stats.items():
            avg_score = sum(stats['scores']) / len(stats['scores'])
            leaderboard.append({
                'model_name': model_name,
                'average_score': round(avg_score, 3),
                'sample_count': stats['count'],
                'min_score': round(min(stats['scores']), 3),
                'max_score': round(max(stats['scores']), 3)
            })

        # Sort by average score descending
        leaderboard.sort(key=lambda x: x['average_score'], reverse=True)
        return leaderboard

    def generate_comparison_table(self) -> str:
        """Generate HTML comparison table of all models."""
        leaderboard = self.generate_leaderboard()

        if not leaderboard:
            return "<p>No data available</p>"

        html = """
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th>Rank</th>
                    <th>Model</th>
                    <th>Average Score</th>
                    <th>Samples</th>
                    <th>Score Range</th>
                </tr>
            </thead>
            <tbody>
        """

        for i, model in enumerate(leaderboard, 1):
            html += f"""
                <tr>
                    <td>{i}</td>
                    <td>{model['model_name']}</td>
                    <td>{model['average_score']:.3f}</td>
                    <td>{model['sample_count']}</td>
                    <td>{model['min_score']:.3f} - {model['max_score']:.3f}</td>
                </tr>
            """

        html += """
            </tbody>
        </table>
        """

        return html

    def generate_detailed_report(self, model_name: str) -> Dict[str, Any]:
        """Generate detailed report for a specific model."""
        model_results = [
            r for r in self.results_data
            if r.get('model_name') == model_name
        ]

        if not model_results:
            return {"error": f"No data found for model: {model_name}"}

        # Calculate statistics
        scores = [r.get('standard_composite_score', 0) for r in model_results]
        llm_scores = [r.get('llm_consensus_score', 0) for r in model_results]
        test_scores = [r.get('test_pass_rate', 0) for r in model_results]

        report = {
            "model_name": model_name,
            "total_evaluations": len(model_results),
            "average_composite_score": round(sum(scores) / len(scores), 3),
            "average_llm_score": round(sum(llm_scores) / len(llm_scores), 3),
            "average_test_score": round(sum(test_scores) / len(test_scores), 3),
            "score_distribution": {
                "min": round(min(scores), 3),
                "max": round(max(scores), 3),
                "median": round(sorted(scores)[len(scores)//2], 3)
            },
            "recent_evaluations": model_results[-5:]  # Last 5 evaluations
        }

        return report

    def export_dashboard_html(self, output_file: str = "dashboard.html"):
        """Export complete dashboard as HTML file."""
        output_path = os.path.join(self.results_dir, output_file)

        leaderboard = self.generate_leaderboard()
        comparison_table = self.generate_comparison_table()

        # Calculate summary statistics
        total_evaluations = len(self.results_data)
        unique_models = len(set(r.get('model_name', 'unknown') for r in self.results_data))

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>LLM Evaluation Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .metric {{ display: inline-block; margin: 10px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2c5aa0; }}
                .metric-label {{ font-size: 14px; color: #666; }}
            </style>
        </head>
        <body>
            <h1>🤖 LLM Evaluation Dashboard</h1>

            <div class="summary">
                <h2>📊 Summary Statistics</h2>
                <div class="metric">
                    <div class="metric-value">{total_evaluations}</div>
                    <div class="metric-label">Total Evaluations</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{unique_models}</div>
                    <div class="metric-label">Unique Models</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{len(leaderboard)}</div>
                    <div class="metric-label">Models with Data</div>
                </div>
            </div>

            <h2>🏆 Model Leaderboard</h2>
            {comparison_table}

            <h2>📈 Detailed Model Reports</h2>
        """

        # Add detailed reports for top models
        for i, model in enumerate(leaderboard[:5], 1):  # Top 5 models
            report = self.generate_detailed_report(model['model_name'])
            html_content += f"""
            <h3>{i}. {model['model_name']}</h3>
            <ul>
                <li><strong>Average Composite Score:</strong> {report['average_composite_score']:.3f}</li>
                <li><strong>Average LLM Score:</strong> {report['average_llm_score']:.3f}</li>
                <li><strong>Average Test Score:</strong> {report['average_test_score']:.3f}</li>
                <li><strong>Total Evaluations:</strong> {report['total_evaluations']}</li>
                <li><strong>Score Range:</strong> {report['score_distribution']['min']:.3f} - {report['score_distribution']['max']:.3f}</li>
            </ul>
            """

        html_content += f"""
            <hr>
            <p><small>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </body>
        </html>
        """

        try:
            with open(output_path, 'w') as f:
                f.write(html_content)

            logger.info(f"Dashboard exported to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to export dashboard: {e}")
            return None

    def get_model_comparison_data(self) -> Dict[str, Any]:
        """Get data for model comparison charts."""
        if not self.results_data:
            return {"error": "No data available"}

        # Group data by model
        model_data = {}
        for result in self.results_data:
            model_name = result.get('model_name', 'unknown')
            if model_name not in model_data:
                model_data[model_name] = []

            model_data[model_name].append({
                'composite_score': result.get('standard_composite_score', 0),
                'llm_score': result.get('llm_consensus_score', 0),
                'test_score': result.get('test_pass_rate', 0),
                'static_score': result.get('static_analysis_score', 0),
                'problem_id': result.get('problem_id', '')
            })

        # Calculate averages for each model
        comparison_data = {}
        for model_name, results in model_data.items():
            scores = [r['composite_score'] for r in results]
            llm_scores = [r['llm_score'] for r in results]
            test_scores = [r['test_score'] for r in results]
            static_scores = [r['static_score'] for r in results]

            comparison_data[model_name] = {
                'average_composite': round(sum(scores) / len(scores), 3),
                'average_llm': round(sum(llm_scores) / len(llm_scores), 3),
                'average_test': round(sum(test_scores) / len(test_scores), 3),
                'average_static': round(sum(static_scores) / len(static_scores), 3),
                'sample_count': len(results),
                'scores': scores  # For distribution analysis
            }

        return comparison_data

    def generate_performance_report(self) -> str:
        """Generate a text-based performance report."""
        if not self.results_data:
            return "No evaluation data available."

        leaderboard = self.generate_leaderboard()
        comparison_data = self.get_model_comparison_data()

        report = f"""
LLM Evaluation Performance Report
==================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS
------------------
Total Evaluations: {len(self.results_data)}
Unique Models: {len(comparison_data)}
Models with Data: {len(leaderboard)}

MODEL LEADERBOARD
------------------
"""

        for i, model in enumerate(leaderboard, 1):
            report += f"{i:2d}. {model['model_name']:<25} "
            report += f"Avg: {model['average_score']:.3f} "
            report += f"Samples: {model['sample_count']:>3d} "
            report += f"Range: {model['min_score']:.3f}-{model['max_score']:.3f}\n"

        report += "\nDETAILED BREAKDOWN\n------------------\n"

        for model_name, data in comparison_data.items():
            report += f"\n{model_name}:\n"
            report += f"  Composite Score: {data['average_composite']:.3f}\n"
            report += f"  LLM Consensus:   {data['average_llm']:.3f}\n"
            report += f"  Test Pass Rate:  {data['average_test']:.3f}\n"
            report += f"  Static Analysis: {data['average_static']:.3f}\n"
            report += f"  Sample Count:    {data['sample_count']}\n"

        return report
"""
Configuration settings for HumanEvalComm Leaderboard
"""
import os


class Config:
    """Application configuration."""

    # Flask settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 8080

    # Data settings
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    LEADERBOARD_PATTERN = 'v2_*leaderboard*.csv'
    RESULTS_PATTERN = 'v2_*results*.json'
    PROBLEMS_FILE = os.path.join(BASE_DIR, 'Benchmark',
                                 'HumanEvalComm_v2.jsonl')

    # Cache settings
    CACHE_ENABLED = True

    # Chart settings
    DEFAULT_CHART_COLORS = [
        '#2563eb',  # blue-600
        '#059669',  # emerald-600
        '#d97706',  # amber-600
        '#dc2626',  # red-600
        '#0891b2',  # cyan-600
        '#7c3aed'   # purple-600
    ]

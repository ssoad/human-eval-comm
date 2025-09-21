# HumanEvalComm V2 Enhanced Interactive Leaderboard

A robust, interactive Flask web application for visualizing HumanEvalComm V2 benchmark results with advanced features and modern UI.

## 🚀 Features

### Core Features
- **Auto-Detection**: Automatically finds and loads the latest leaderboard and results files
- **Interactive Charts**: Real-time Plotly charts for data visualization
- **Advanced Filtering**: Filter by model, problem, prompt type, and more
- **Sorting**: Sort by any column in ascending or descending order
- **Responsive Design**: Modern Bootstrap UI that works on all devices
- **Real-time Updates**: Auto-refresh data every 5 minutes
- **Detailed View**: Comprehensive evaluation details with code preview

### V2 Benchmark Integration
- **Enhanced Aggregation**: Displays V2 composite scores and formulas used
- **Multi-LLM Judging**: Shows consensus scores and judge confidence
- **Hypothesis Fuzzing**: Displays fuzz test results and coverage improvement
- **Communication Metrics**: Visualizes question rates and quality
- **Error Handling**: Robust error handling with helpful troubleshooting

### Interactive Elements
- **Dynamic Charts**: V2 score comparison, communication metrics, performance radar
- **Code Preview**: Click to view full code and responses in modals
- **Live Filtering**: Real-time table filtering and sorting
- **Data Refresh**: Manual and automatic data refresh capabilities
- **File Management**: View available files and their timestamps

## 📦 Installation

1. **Install dependencies:**
   ```bash
   cd flask_leaderboard
   pip install -r requirements_enhanced.txt
   ```

2. **Run the enhanced app:**
   ```bash
   python app_enhanced.py
   ```

3. **Open your browser:**
   Navigate to [http://localhost:5000](http://localhost:5000)

## 🎯 Usage

### Main Leaderboard (`/`)
- View comprehensive leaderboard with all V2 metrics
- Interactive charts showing model performance
- Filter by model and sort by any metric
- Real-time summary statistics
- Professional table with color-coded scores

### Detailed Results (`/detailed`)
- Individual evaluation results for each problem
- Filter by model and problem
- View full code and responses
- Detailed V2 evaluation metrics
- Multi-LLM judge scores and confidence

### API Endpoints
- `/api/data` - JSON leaderboard data
- `/api/charts` - Chart data for visualizations
- `/refresh` - Refresh data cache
- `/files` - List available files

## 🔧 Configuration

### Auto-Detection
The app automatically detects the latest files matching these patterns:
- Leaderboard: `v2_*leaderboard*.csv`
- Results: `v2_*results*.json`

### Customization
- **Update file patterns** in `LeaderboardManager.find_latest_files()`
- **Modify chart types** in the `/api/charts` endpoint
- **Customize UI colors** in the CSS styles
- **Add new metrics** by extending the template logic

## 📊 Charts & Visualizations

### V2 Score Comparison
- Bar chart comparing V2 composite scores across models
- Color-coded bars for easy identification
- Interactive hover tooltips

### Communication Metrics
- Grouped bar chart showing communication rate and question quality
- Side-by-side comparison of models
- Percentage-based visualization

### Performance Radar Chart
- Multi-dimensional radar chart showing all performance metrics
- Overlaid model comparisons
- Normalized scales for fair comparison

## 🛠️ Troubleshooting

### Common Issues

1. **No data found:**
   ```bash
   # Run the V2 benchmark first
   python v2_benchmark_completely_fixed.py
   ```

2. **File permission errors:**
   ```bash
   chmod 644 v2_*.csv v2_*.json
   ```

3. **Missing dependencies:**
   ```bash
   pip install -r requirements_enhanced.txt
   ```

4. **Port already in use:**
   ```bash
   # Change port in app_enhanced.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Data Refresh
- **Manual**: Click the refresh button or visit `/refresh`
- **Automatic**: Data refreshes every 5 minutes
- **Cache**: File-based caching with modification time checking

## 🚀 Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_enhanced.txt .
RUN pip install -r requirements_enhanced.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_enhanced:app"]
```

## 📈 Performance Features

- **Caching**: Intelligent file-based caching with modification time checking
- **Lazy Loading**: Charts load asynchronously for faster page loads
- **Responsive**: Optimized for mobile and desktop viewing
- **Error Recovery**: Graceful handling of missing or corrupted data files

## 🎨 UI/UX Features

- **Modern Design**: Gradient backgrounds and card-based layout
- **Color Coding**: Score-based color coding for quick assessment
- **Icons**: Font Awesome icons for better visual hierarchy
- **Animations**: Smooth transitions and hover effects
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 🔗 Integration

The enhanced leaderboard seamlessly integrates with:
- **V2 Benchmark Script**: `v2_benchmark_completely_fixed.py`
- **Enhanced Aggregator**: Displays formula and penalty/bonus information
- **Multi-LLM Judge**: Shows consensus scores and judge details
- **Hypothesis Fuzzer**: Displays fuzz test results and coverage

## 📝 API Documentation

### GET `/api/data`
Returns complete leaderboard data in JSON format.

### GET `/api/charts`
Returns chart data for visualizations.

### GET `/refresh`
Clears cache and refreshes data.

### GET `/files`
Lists all available leaderboard and results files.

## 🎯 Next Steps

- Add real-time WebSocket updates
- Implement user authentication
- Add export functionality (PDF, Excel)
- Create custom dashboard builder
- Add model comparison tools
- Implement historical trend analysis

Happy benchmarking! 🚀
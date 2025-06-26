# Metrics Comparison Tool 📊

A beautiful console application for comparing two `aggregate_metrics.json` files with fancy visualization that highlights changes whether they're increasing, decreasing, or the same.

## Features ✨

- **🎨 Beautiful Console Output**: Rich formatting with colors, tables, and symbols
- **📈 Change Detection**: Automatically detects increases, decreases, and unchanged values
- **📊 Multiple View Formats**: Table and tree view options
- **💯 Percentage Changes**: Shows percentage change for numeric values
- **🔍 Detailed Analysis**: Comprehensive comparison of all metrics
- **📅 Metadata Comparison**: Shows file generation times and source information
- **⚡ Fast Performance**: Efficient comparison algorithm

## Installation 🚀

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Make Script Executable** (optional):
   ```bash
   chmod +x metrics_comparator.py
   ```

## Usage 💻

### Basic Comparison
```bash
python metrics_comparator.py old_metrics.json new_metrics.json
```

### Show Unchanged Values
```bash
python metrics_comparator.py -u old_metrics.json new_metrics.json
```

### Tree View Format
```bash
python metrics_comparator.py -f tree old_metrics.json new_metrics.json
```

### Help
```bash
python metrics_comparator.py --help
```

## Command Line Options 🛠️

| Option | Description |
|--------|-------------|
| `file1` | Path to the first (old) metrics file |
| `file2` | Path to the second (new) metrics file |
| `-u, --show-unchanged` | Show unchanged metrics in the output |
| `-f, --format` | Output format: `table` (default) or `tree` |
| `-h, --help` | Show help message |

## Output Explanation 📋

### Symbols Used
- 📈 **Increased**: Value has gone up
- 📉 **Decreased**: Value has gone down  
- ➡️ **Unchanged**: Value remained the same
- ✨ **New**: Metric appears in new file only
- ❌ **Removed**: Metric appears in old file only

### Color Coding
- 🟢 **Green**: Increased values
- 🔴 **Red**: Decreased values  
- 🔵 **Blue**: Unchanged values
- 🟡 **Yellow**: New metrics

### View Formats

#### Table View (Default)
- Detailed tabular comparison
- Shows all metrics with old/new values
- Includes percentage changes
- Sortable by metric name

#### Tree View
- Hierarchical grouping by metric categories
- Summary counts for each metric group
- Compact representation of changes
- Excludes unchanged values for clarity

## Sample Output 📸

```
🚀 Metrics Comparison Tool

📊 Total Metrics: 154
📈 Increased: 49  📉 Decreased: 54  ➡️ Unchanged: 45
✨ New: 6  ❌ Removed: 0

┌──────────────────────────────────┬────────────────────────┬──────────────┬───────────┬───────────┬────────────┐
│ Metric                           │ Field                  │    Status    │ Old Value │ New Value │     Change │
├──────────────────────────────────┼────────────────────────┼──────────────┼───────────┼───────────┼────────────┤
│ what_rouge1_f1                   │ mean                   │ 📈 Increased │  0.15148  │  0.16148  │   (+6.60%) │
│ what_rouge1_precision            │ mean                   │ 📉 Decreased │  0.10596  │  0.09596  │   (-9.44%) │
└──────────────────────────────────┴────────────────────────┴──────────────┴───────────┴───────────┴────────────┘
```

## File Format 📝

The tool expects JSON files with the following structure:

```json
{
  "aggregate_metrics": {
    "metric_name": {
      "mean": 1.23,
      "median": 1.0,
      "std_dev": 0.45,
      "min": 1.0,
      "max": 2.0,
      "count": 56
    }
  },
  "metadata": {
    "generated_at": "2025-06-26T06:32:28.847606",
    "source_file": "path/to/source.json",
    "description": "Description of the metrics"
  }
}
```

## Requirements 📦

- Python 3.7+
- rich >= 13.0.0

## Examples 🔧

### Compare Two Files
```bash
python metrics_comparator.py metrics_v1.json metrics_v2.json
```

### Tree View with All Changes
```bash
python metrics_comparator.py -f tree -u old.json new.json
```

### Quick Check for Changes
```bash
python metrics_comparator.py baseline.json latest.json | grep -E "(Increased|Decreased)"
```

## Tips 💡

1. **Large Files**: The tool handles large JSON files efficiently
2. **Precision**: Floating-point comparisons account for precision errors
3. **Missing Values**: Gracefully handles missing metrics between files
4. **Colors**: Best viewed in terminals that support true color
5. **Export**: Pipe output to files for reports: `python metrics_comparator.py file1.json file2.json > report.txt`

## Troubleshooting 🔧

### Common Issues

1. **File Not Found**: Ensure file paths are correct
2. **Invalid JSON**: Check JSON syntax with a validator
3. **No Changes Shown**: Use `-u` flag to see unchanged values
4. **Colors Not Showing**: Update terminal or use a different console

### Error Messages

- `❌ File not found`: Check file path
- `❌ Invalid JSON`: Validate JSON syntax
- `❌ Required package 'rich' not found`: Run `pip install rich`

---

Made with ❤️ for better metrics analysis

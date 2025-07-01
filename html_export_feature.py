#!/usr/bin/env python3
"""
HTML Export Feature for Metrics Comparison Tool
Converts Rich console output to beautiful HTML with full styling preservation
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from io import StringIO
import html
import re
from datetime import datetime

class HTMLExporter:
    def __init__(self):
        self.console = Console(record=True, width=120)
        
    def export_to_html(self, comparison_data, output_file="comparison_report.html"):
        """Export comparison to a beautiful HTML file"""
        
        # Capture the rich output
        with self.console.capture() as capture:
            # Re-render the comparison (you'd call your existing comparison methods here)
            self._render_comparison_for_html(comparison_data)
        
        html_content = self.console.export_html(
            title="Metrics Comparison Report",
            code_format="""
            <style>
                body { 
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace; 
                    background: #1e1e1e; 
                    color: #d4d4d4; 
                    margin: 20px;
                    line-height: 1.4;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: #252526; 
                    padding: 20px; 
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                }
                h1 { 
                    color: #4FC3F7; 
                    text-align: center; 
                    margin-bottom: 30px;
                    font-size: 24px;
                }
                .timestamp { 
                    text-align: center; 
                    color: #888; 
                    margin-bottom: 20px; 
                }
                .rich-terminal { 
                    background: #0d1117 !important; 
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 16px;
                }
                /* Custom emoji and symbol styling */
                .increase { color: #4ade80; }
                .decrease { color: #f87171; }
                .unchanged { color: #60a5fa; }
                .new { color: #fbbf24; }
                .removed { color: #f87171; }
            </style>
            """
        )
        
        # Wrap in a nice container
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Metrics Comparison Report</title>
        </head>
        <body>
            <div class="container">
                <h1>📊 Metrics Comparison Report</h1>
                <div class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                {html_content}
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return output_file
    
    def _render_comparison_for_html(self, comparison_data):
        """Render comparison data for HTML capture"""
        # This would be your existing rendering logic
        pass

# Example usage:
# exporter = HTMLExporter()
# exporter.export_to_html(comparison_data, "metrics_report.html")

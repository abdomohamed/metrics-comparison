#!/usr/bin/env python3
"""
Metrics Comparison Tool with Fancy Visualization

A console application that compares two aggregate_metrics.json files and
highlights changes with beautiful visualization.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.tree import Tree
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.align import Align
    import rich.box
except ImportError:
    print("❌ Required package 'rich' not found. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.tree import Tree
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.align import Align
    import rich.box


class ChangeType(Enum):
    INCREASED = "increased"
    DECREASED = "decreased"
    UNCHANGED = "unchanged"
    NEW = "new"
    REMOVED = "removed"


@dataclass
class MetricChange:
    metric_name: str
    field_name: str
    old_value: Optional[float]
    new_value: Optional[float]
    change_type: ChangeType
    percentage_change: Optional[float] = None

    def __post_init__(self):
        if self.old_value is not None and self.new_value is not None and self.old_value != 0:
            self.percentage_change = ((self.new_value - self.old_value) / self.old_value) * 100


class MetricsComparator:
    def __init__(self):
        self.console = Console()

    def load_json_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.console.print(f"❌ [red]File not found: {file_path}[/red]")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.console.print(f"❌ [red]Invalid JSON in {file_path}: {e}[/red]")
            sys.exit(1)

    def compare_metrics(self, old_data: Dict[str, Any], new_data: Dict[str, Any]) -> list[MetricChange]:
        """Compare two metrics dictionaries and return list of changes."""
        changes = []
        
        old_metrics = old_data.get("aggregate_metrics", {})
        new_metrics = new_data.get("aggregate_metrics", {})
        
        # Get all metric names from both datasets
        all_metrics = set(old_metrics.keys()) | set(new_metrics.keys())
        
        for metric_name in all_metrics:
            old_metric = old_metrics.get(metric_name, {})
            new_metric = new_metrics.get(metric_name, {})
            
            if metric_name not in old_metrics:
                # New metric
                for field_name, new_value in new_metric.items():
                    if isinstance(new_value, (int, float)):
                        changes.append(MetricChange(
                            metric_name=metric_name,
                            field_name=field_name,
                            old_value=None,
                            new_value=new_value,
                            change_type=ChangeType.NEW
                        ))
            elif metric_name not in new_metrics:
                # Removed metric
                for field_name, old_value in old_metric.items():
                    if isinstance(old_value, (int, float)):
                        changes.append(MetricChange(
                            metric_name=metric_name,
                            field_name=field_name,
                            old_value=old_value,
                            new_value=None,
                            change_type=ChangeType.REMOVED
                        ))
            else:
                # Compare existing metrics
                all_fields = set(old_metric.keys()) | set(new_metric.keys())
                
                for field_name in all_fields:
                    old_value = old_metric.get(field_name)
                    new_value = new_metric.get(field_name)
                    
                    # Only compare numeric values
                    if not (isinstance(old_value, (int, float)) and isinstance(new_value, (int, float))):
                        continue
                    
                    if old_value is None:
                        change_type = ChangeType.NEW
                    elif new_value is None:
                        change_type = ChangeType.REMOVED
                    elif abs(new_value - old_value) < 1e-10:  # Account for floating point precision
                        change_type = ChangeType.UNCHANGED
                    elif new_value > old_value:
                        change_type = ChangeType.INCREASED
                    else:
                        change_type = ChangeType.DECREASED
                    
                    changes.append(MetricChange(
                        metric_name=metric_name,
                        field_name=field_name,
                        old_value=old_value,
                        new_value=new_value,
                        change_type=change_type
                    ))
        
        return changes

    def get_change_symbol_and_color(self, change: MetricChange) -> Tuple[str, str]:
        """Get symbol and color for a change type."""
        symbols_colors = {
            ChangeType.INCREASED: ("📈", "green"),
            ChangeType.DECREASED: ("📉", "red"),
            ChangeType.UNCHANGED: ("➡️", "blue"),
            ChangeType.NEW: ("✨", "yellow"),
            ChangeType.REMOVED: ("❌", "red")
        }
        return symbols_colors.get(change.change_type, ("❓", "white"))

    def format_value(self, value: Optional[float]) -> str:
        """Format a numeric value for display."""
        if value is None:
            return "N/A"
        if isinstance(value, int) or value.is_integer():
            return str(int(value))
        return f"{value:.6f}".rstrip('0').rstrip('.')

    def format_percentage_change(self, change: MetricChange) -> str:
        """Format percentage change for display."""
        if change.percentage_change is None:
            return ""
        
        abs_change = abs(change.percentage_change)
        if abs_change < 0.01:
            return ""
        
        sign = "+" if change.percentage_change > 0 else ""
        return f" ({sign}{change.percentage_change:.2f}%)"

    def create_summary_panel(self, changes: list[MetricChange]) -> Panel:
        """Create a summary panel with change statistics."""
        total_changes = len(changes)
        increased = sum(1 for c in changes if c.change_type == ChangeType.INCREASED)
        decreased = sum(1 for c in changes if c.change_type == ChangeType.DECREASED)
        unchanged = sum(1 for c in changes if c.change_type == ChangeType.UNCHANGED)
        new = sum(1 for c in changes if c.change_type == ChangeType.NEW)
        removed = sum(1 for c in changes if c.change_type == ChangeType.REMOVED)

        summary_text = Text()
        summary_text.append("📊 Total Metrics: ", style="bold")
        summary_text.append(f"{total_changes}\n", style="bold white")
        
        summary_text.append("📈 Increased: ", style="bold")
        summary_text.append(f"{increased}", style="bold green")
        summary_text.append("  📉 Decreased: ", style="bold")
        summary_text.append(f"{decreased}", style="bold red")
        summary_text.append("  ➡️ Unchanged: ", style="bold")
        summary_text.append(f"{unchanged}", style="bold blue")
        summary_text.append("\n✨ New: ", style="bold")
        summary_text.append(f"{new}", style="bold yellow")
        summary_text.append("  ❌ Removed: ", style="bold")
        summary_text.append(f"{removed}", style="bold red")

        return Panel(
            Align.center(summary_text),
            title="📈 [bold]Metrics Comparison Summary[/bold]",
            border_style="cyan",
            box=rich.box.DOUBLE
        )

    def create_detailed_table(self, changes: list[MetricChange], show_unchanged: bool = False) -> Table:
        """Create a detailed table of all changes."""
        table = Table(
            title="🔍 [bold]Detailed Metrics Comparison[/bold]",
            box=rich.box.ROUNDED,
            header_style="bold magenta"
        )
        
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Field", style="yellow")
        table.add_column("Status", justify="center")
        table.add_column("Old Value", justify="right", style="dim")
        table.add_column("New Value", justify="right", style="bright_white")
        table.add_column("Change", justify="right")

        # Filter changes if needed
        filtered_changes = changes
        if not show_unchanged:
            filtered_changes = [c for c in changes if c.change_type != ChangeType.UNCHANGED]

        # Sort changes by metric name, then by field name
        filtered_changes.sort(key=lambda x: (x.metric_name, x.field_name))

        for change in filtered_changes:
            symbol, color = self.get_change_symbol_and_color(change)
            
            old_value_str = self.format_value(change.old_value)
            new_value_str = self.format_value(change.new_value)
            percentage_str = self.format_percentage_change(change)
            
            status_text = Text(f"{symbol} {change.change_type.value.title()}")
            status_text.stylize(color)
            
            table.add_row(
                change.metric_name,
                change.field_name,
                status_text,
                old_value_str,
                new_value_str,
                percentage_str
            )

        return table

    def create_metrics_tree(self, changes: list[MetricChange]) -> Tree:
        """Create a tree view grouped by metrics."""
        tree = Tree("📊 [bold cyan]Metrics Overview[/bold cyan]")
        
        # Group changes by metric name
        metrics_dict = {}
        for change in changes:
            if change.metric_name not in metrics_dict:
                metrics_dict[change.metric_name] = []
            metrics_dict[change.metric_name].append(change)
        
        for metric_name, metric_changes in sorted(metrics_dict.items()):
            # Count change types for this metric
            increased = sum(1 for c in metric_changes if c.change_type == ChangeType.INCREASED)
            decreased = sum(1 for c in metric_changes if c.change_type == ChangeType.DECREASED)
            unchanged = sum(1 for c in metric_changes if c.change_type == ChangeType.UNCHANGED)
            new = sum(1 for c in metric_changes if c.change_type == ChangeType.NEW)
            removed = sum(1 for c in metric_changes if c.change_type == ChangeType.REMOVED)
            
            # Create metric node with summary
            metric_text = Text(metric_name, style="bold white")
            if increased > 0:
                metric_text.append(f" 📈{increased}", style="green")
            if decreased > 0:
                metric_text.append(f" 📉{decreased}", style="red")
            if new > 0:
                metric_text.append(f" ✨{new}", style="yellow")
            if removed > 0:
                metric_text.append(f" ❌{removed}", style="red")
            
            metric_node = tree.add(metric_text)
            
            # Add field changes
            for change in sorted(metric_changes, key=lambda x: x.field_name):
                if change.change_type == ChangeType.UNCHANGED:
                    continue  # Skip unchanged in tree view
                
                symbol, color = self.get_change_symbol_and_color(change)
                field_text = Text(f"{symbol} {change.field_name}: ")
                field_text.append(f"{self.format_value(change.old_value)} → {self.format_value(change.new_value)}")
                field_text.append(self.format_percentage_change(change), style="dim")
                field_text.stylize(color)
                
                metric_node.add(field_text)
        
        return tree

    def compare_files(self, file1: str, file2: str, show_unchanged: bool = False, output_format: str = "table"):
        """Main comparison function."""
        self.console.print("\n🚀 [bold cyan]Metrics Comparison Tool[/bold cyan]\n")
        
        # Show progress while loading
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Loading files...", total=None)
            
            self.console.print(f"📁 Loading file 1: [yellow]{file1}[/yellow]")
            old_data = self.load_json_file(file1)
            
            self.console.print(f"📁 Loading file 2: [yellow]{file2}[/yellow]")
            new_data = self.load_json_file(file2)
            
            progress.update(task, description="Comparing metrics...")
            changes = self.compare_metrics(old_data, new_data)
            
            progress.update(task, description="Generating visualization...")

        self.console.print()
        
        # Display summary
        summary_panel = self.create_summary_panel(changes)
        self.console.print(summary_panel)
        self.console.print()

        # Display detailed comparison based on format
        if output_format == "tree":
            tree = self.create_metrics_tree(changes)
            self.console.print(tree)
        else:  # table format
            table = self.create_detailed_table(changes, show_unchanged)
            self.console.print(table)

        # Show metadata comparison if available
        self._show_metadata_comparison(old_data, new_data)

    def _show_metadata_comparison(self, old_data: Dict[str, Any], new_data: Dict[str, Any]):
        """Show metadata comparison in a panel."""
        old_meta = old_data.get("metadata", {})
        new_meta = new_data.get("metadata", {})
        
        if not old_meta and not new_meta:
            return
        
        meta_text = Text()
        meta_text.append("📅 Generation Times:\n", style="bold")
        
        old_time = old_meta.get("generated_at", "N/A")
        new_time = new_meta.get("generated_at", "N/A")
        
        meta_text.append(f"  Old: {old_time}\n", style="dim")
        meta_text.append(f"  New: {new_time}\n", style="bright_white")
        
        if old_meta.get("source_file") or new_meta.get("source_file"):
            meta_text.append("\n📄 Source Files:\n", style="bold")
            meta_text.append(f"  Old: {old_meta.get('source_file', 'N/A')}\n", style="dim")
            meta_text.append(f"  New: {new_meta.get('source_file', 'N/A')}", style="bright_white")

        meta_panel = Panel(
            meta_text,
            title="ℹ️ [bold]Metadata[/bold]",
            border_style="blue",
            box=rich.box.ROUNDED
        )
        
        self.console.print()
        self.console.print(meta_panel)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two aggregate_metrics.json files with fancy visualization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s old_metrics.json new_metrics.json
  %(prog)s -u old_metrics.json new_metrics.json    # Show unchanged values
  %(prog)s -f tree old_metrics.json new_metrics.json  # Tree format
        """
    )
    
    parser.add_argument("file1", help="Path to the first (old) metrics file")
    parser.add_argument("file2", help="Path to the second (new) metrics file")
    parser.add_argument(
        "-u", "--show-unchanged",
        action="store_true",
        help="Show unchanged metrics in the output"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["table", "tree"],
        default="table",
        help="Output format (default: table)"
    )

    args = parser.parse_args()

    # Validate files exist
    for file_path in [args.file1, args.file2]:
        if not Path(file_path).exists():
            print(f"❌ Error: File '{file_path}' does not exist.")
            sys.exit(1)

    comparator = MetricsComparator()
    comparator.compare_files(
        args.file1,
        args.file2,
        show_unchanged=args.show_unchanged,
        output_format=args.format
    )


if __name__ == "__main__":
    main()

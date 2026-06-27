"""
Main Entry Point

This is the main module that orchestrates the student result analysis workflow.
"""

import sys
import pandas as pd
from pathlib import Path
from analyzer import StudentResultAnalyzer
from report import ReportGenerator


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load student data from file.
    
    Args:
        file_path: Path to data file (Excel or CSV)
        
    Returns:
        DataFrame with student data
    """
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Use .xlsx, .xls, or .csv")
        
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def ensure_output_directory() -> None:
    """Ensure output directory exists."""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)


def main():
    """Main function to run the student result analyzer."""
    
    print("=" * 60)
    print("Student Result Analyzer")
    print("=" * 60)
    
    # Ensure output directory exists
    ensure_output_directory()
    
    # Get input file from user or use default
    data_file = input("\nEnter path to student results file (or press Enter for data/results.xlsx): ").strip()
    if not data_file:
        data_file = 'data/results.xlsx'
    
    # Load data
    print(f"\nLoading data from {data_file}...")
    data = load_data(data_file)
    print(f"✓ Loaded {len(data)} student records")
    
    # Initialize analyzer
    print("\nAnalyzing student results...")
    analyzer = StudentResultAnalyzer(data)
    summary = analyzer.performance_summary()
    
    # Display summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Students: {summary['total_students']}")
    print(f"Pass Rate: {summary['pass_rate']:.2f}%")
    
    # Generate reports
    print("\nGenerating reports...")
    report_gen = ReportGenerator(analyzer)
    
    # Export to HTML
    report_gen.export_to_html('output/report.html')
    
    # Export to Excel
    try:
        report_gen.export_to_excel('output/report.xlsx')
    except ImportError:
        print("Note: openpyxl not installed. Excel export skipped.")
    
    print("\n" + "=" * 60)
    print("✓ Analysis complete! Reports generated in 'output/' directory")
    print("=" * 60)


if __name__ == '__main__':
    main()

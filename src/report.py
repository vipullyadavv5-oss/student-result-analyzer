"""
Report Generation Module

This module handles the creation of reports from analyzed student data.
"""

import pandas as pd
from typing import Dict, Any
from datetime import datetime


class ReportGenerator:
    """Generates reports from student analysis data."""

    def __init__(self, analyzer: Any):
        """
        Initialize report generator.
        
        Args:
            analyzer: StudentResultAnalyzer instance
        """
        self.analyzer = analyzer
        self.report_data = {}

    def generate_summary_report(self) -> Dict:
        """
        Generate a summary report of student performance.
        
        Returns:
            Dictionary containing the report data
        """
        summary = self.analyzer.performance_summary()
        
        report = {
            'title': 'Student Result Analysis Report',
            'generated_at': datetime.now().isoformat(),
            'summary': summary,
            'grade_distribution': self.analyzer.grade_distribution(),
            'recommendations': self._generate_recommendations(summary)
        }
        
        return report

    def _generate_recommendations(self, summary: Dict) -> List[str]:
        """
        Generate recommendations based on analysis.
        
        Args:
            summary: Performance summary dictionary
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        pass_rate = summary.get('pass_rate', 0)
        if pass_rate < 50:
            recommendations.append('Low pass rate detected. Additional support needed.')
        elif pass_rate > 90:
            recommendations.append('Excellent pass rate. Maintain current strategies.')
        
        if summary.get('total_students', 0) > 0:
            recommendations.append('Review top performers for mentorship opportunities.')
        
        return recommendations

    def export_to_html(self, output_path: str = 'output/report.html') -> None:
        """
        Export report to HTML format.
        
        Args:
            output_path: Path to save HTML report
        """
        report = self.generate_summary_report()
        html_content = self._create_html_content(report)
        
        try:
            with open(output_path, 'w') as f:
                f.write(html_content)
            print(f"Report exported to {output_path}")
        except Exception as e:
            print(f"Error exporting report: {e}")

    def _create_html_content(self, report: Dict) -> str:
        """
        Create HTML content for the report.
        
        Args:
            report: Report data dictionary
            
        Returns:
            HTML string
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                .recommendation {{ background: #e8f5e9; padding: 10px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>{report['title']}</h1>
            <p>Generated: {report['generated_at']}</p>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Students: {report['summary'].get('total_students', 0)}</p>
                <p>Pass Rate: {report['summary'].get('pass_rate', 0):.2f}%</p>
            </div>
            
            <h2>Recommendations</h2>
            {"".join(f'<div class="recommendation">{rec}</div>' for rec in report['recommendations'])}
        </body>
        </html>
        """
        return html

    def export_to_excel(self, output_path: str = 'output/report.xlsx') -> None:
        """
        Export report to Excel format.
        
        Args:
            output_path: Path to save Excel report
        """
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                summary_df = pd.DataFrame([self.analyzer.performance_summary()])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                stats = self.analyzer.calculate_statistics()
                stats_df = pd.DataFrame(stats)
                stats_df.to_excel(writer, sheet_name='Statistics')
                
            print(f"Report exported to {output_path}")
        except Exception as e:
            print(f"Error exporting report: {e}")

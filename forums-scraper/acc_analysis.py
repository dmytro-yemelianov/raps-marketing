#!/usr/bin/env python3
"""
ACC Forum Analysis Script

Analyzes feature requests from Autodesk Construction Cloud Ideas Forum.
Part of the raps-research repository: https://github.com/dmytro-yemelianov/raps-research

Usage:
    python analysis.py --input acc_ideas.csv --output results/

Requirements:
    pip install pandas matplotlib seaborn
"""

import pandas as pd
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
import re


# Topic categories for classification
TOPIC_KEYWORDS = {
    'User Management & Permissions': ['user', 'permission', 'access', 'role', 'member', 'admin', 'invite'],
    'Photos & Media': ['photo', 'image', 'picture', 'camera', 'media'],
    'Viewer & 3D': ['viewer', '3d', 'view', 'model', 'section', 'measure', 'coordinate', 'navigation'],
    'Documents & Files': ['document', 'doc', 'file', 'upload', 'download', 'pdf', 'folder', 'naming'],
    'Markups & Annotations': ['markup', 'annotation', 'comment', 'redline'],
    'Submittals & RFIs': ['submittal', 'rfi', 'review', 'approval', 'workflow'],
    'Issues & Tasks': ['issue', 'task', 'checklist', 'punch', 'defect'],
    'Notifications & Email': ['notification', 'email', 'alert', 'reminder'],
    'Integration & Sync': ['integration', 'sync', 'connector', 'desktop', 'revit', 'excel', 'office'],
    'Reports & Export': ['report', 'export', 'dashboard', 'analytics', 'csv'],
    'Design Collaboration': ['design collaboration', 'publish', 'package', 'team', 'collaboration'],
    'Sheets & Drawing': ['sheet', 'drawing', 'plan', 'version'],
    'Model Coordination': ['coordination', 'clash', 'navisworks'],
    'Assets & Tracking': ['asset', 'barcode', 'tracking', 'inventory'],
    'API & Automation': ['api', 'automate', 'automation', 'script', 'webhook'],
    'Mobile App': ['mobile', 'app', 'ios', 'android', 'offline'],
    'Cost & Budget': ['cost', 'budget', 'estimate', 'pricing'],
    'Templates & Standards': ['template', 'standard', 'default'],
}

PAIN_PATTERNS = {
    'bulk_batch': ['bulk', 'batch', 'multiple', 'mass'],
    'performance': ['slow', 'performance', 'speed', 'faster', 'loading'],
    'offline': ['offline', 'internet', 'connection'],
    'export': ['export', 'csv', 'excel'],
    'permissions': ['permission', 'access', 'restrict', 'inherit'],
    'notifications': ['notification', 'email', 'spam', 'alert'],
    'sync': ['sync', 'synchron', 'connector'],
    'missing_features': ['need', 'required', 'missing', 'lack'],
    'ux_workflow': ['click', 'workflow', 'easier', 'streamline', 'intuitive'],
}


def load_data(filepath: str) -> pd.DataFrame:
    """Load and preprocess the CSV data."""
    df = pd.read_csv(filepath)
    
    # Parse dates
    df['post_date'] = pd.to_datetime(df['post_date'])
    df['year'] = df['post_date'].dt.year
    df['year_month'] = df['post_date'].dt.to_period('M')
    
    return df


def categorize_idea(row: pd.Series) -> list:
    """Assign topic categories to an idea based on keywords."""
    text = (str(row['title']) + ' ' + str(row['body_text'])).lower()
    categories = []
    
    for cat, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            categories.append(cat)
    
    return categories if categories else ['Other']


def detect_pain_patterns(row: pd.Series) -> list:
    """Detect pain patterns in an idea."""
    text = (str(row['title']) + ' ' + str(row['body_text'])).lower()
    patterns = []
    
    for pattern, keywords in PAIN_PATTERNS.items():
        if any(kw in text for kw in keywords):
            patterns.append(pattern)
    
    return patterns


def analyze_status_distribution(df: pd.DataFrame) -> dict:
    """Analyze the distribution of statuses."""
    status_counts = df['status_name'].value_counts().to_dict()
    total = len(df)
    
    return {
        'counts': status_counts,
        'percentages': {k: round(v / total * 100, 2) for k, v in status_counts.items()},
        'total': total
    }


def analyze_categories(df: pd.DataFrame) -> dict:
    """Analyze ideas by category."""
    df['categories'] = df.apply(categorize_idea, axis=1)
    
    category_stats = {}
    for idx, row in df.iterrows():
        for cat in row['categories']:
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'kudos': 0, 'views': 0}
            category_stats[cat]['count'] += 1
            category_stats[cat]['kudos'] += row['kudos']
            category_stats[cat]['views'] += row['views']
    
    # Calculate averages
    for cat in category_stats:
        count = category_stats[cat]['count']
        category_stats[cat]['avg_kudos'] = round(category_stats[cat]['kudos'] / count, 2) if count > 0 else 0
    
    return category_stats


def analyze_pain_patterns(df: pd.DataFrame) -> dict:
    """Analyze pain pattern frequency."""
    pattern_stats = {p: {'count': 0, 'kudos': 0} for p in PAIN_PATTERNS.keys()}
    
    for idx, row in df.iterrows():
        patterns = detect_pain_patterns(row)
        for p in patterns:
            pattern_stats[p]['count'] += 1
            pattern_stats[p]['kudos'] += row['kudos']
    
    return pattern_stats


def analyze_timeline(df: pd.DataFrame) -> dict:
    """Analyze submission trends over time."""
    yearly = df.groupby('year').agg({
        'id': 'count',
        'kudos': 'sum',
        'views': 'sum'
    }).reset_index()
    
    yearly.columns = ['year', 'ideas', 'kudos', 'views']
    
    return yearly.to_dict('records')


def get_top_ideas(df: pd.DataFrame, n: int = 20) -> list:
    """Get top N ideas by kudos."""
    top = df.nlargest(n, 'kudos')[['id', 'title', 'kudos', 'views', 'status_name', 'post_date']]
    top['post_date'] = top['post_date'].dt.strftime('%Y-%m-%d')
    return top.to_dict('records')


def get_frustration_indicators(df: pd.DataFrame) -> list:
    """Find high-kudos old ideas that haven't been implemented."""
    old_high = df[
        (df['year'] <= 2024) & 
        (df['kudos'] >= 40) & 
        (~df['status_name'].isin(['Implemented']))
    ].nlargest(15, 'kudos')
    
    old_high = old_high[['id', 'title', 'kudos', 'status_name', 'post_date']]
    old_high['post_date'] = old_high['post_date'].dt.strftime('%Y-%m-%d')
    
    return old_high.to_dict('records')


def get_keyword_frequency(df: pd.DataFrame, top_n: int = 30) -> dict:
    """Get most common words in titles."""
    stop_words = {'this', 'that', 'with', 'from', 'have', 'when', 'should', 'would', 
                  'could', 'about', 'which', 'into', 'like', 'more', 'than', 'able',
                  'only', 'them', 'through', 'also', 'being', 'there', 'their', 'they'}
    
    words = []
    for title in df['title'].dropna():
        tokens = re.findall(r'\b[a-zA-Z]{4,}\b', str(title).lower())
        words.extend([t for t in tokens if t not in stop_words])
    
    return dict(Counter(words).most_common(top_n))


def analyze_japanese_market(df: pd.DataFrame) -> dict:
    """Analyze Japanese language submissions."""
    jp_pattern = r'[\u3000-\u9fff]'
    jp_ideas = df[df['title'].str.contains(jp_pattern, regex=True, na=False)]
    
    jp_dates = jp_ideas['post_date'].dt.strftime('%Y-%m-%d').value_counts().head(5).to_dict()
    
    return {
        'total_japanese_ideas': len(jp_ideas),
        'top_submission_dates': jp_dates
    }


def run_full_analysis(input_path: str, output_dir: str = None) -> dict:
    """Run complete analysis and optionally save results."""
    print(f"Loading data from {input_path}...")
    df = load_data(input_path)
    
    print(f"Analyzing {len(df)} ideas...")
    
    results = {
        'metadata': {
            'total_ideas': len(df),
            'date_range': {
                'start': df['post_date'].min().strftime('%Y-%m-%d'),
                'end': df['post_date'].max().strftime('%Y-%m-%d')
            },
            'total_kudos': int(df['kudos'].sum()),
            'total_views': int(df['views'].sum()),
            'analysis_date': datetime.now().isoformat()
        },
        'status_distribution': analyze_status_distribution(df),
        'categories': analyze_categories(df),
        'pain_patterns': analyze_pain_patterns(df),
        'timeline': analyze_timeline(df),
        'top_ideas': get_top_ideas(df, 20),
        'frustration_indicators': get_frustration_indicators(df),
        'keyword_frequency': get_keyword_frequency(df),
        'japanese_market': analyze_japanese_market(df)
    }
    
    # Calculate implementation rate
    impl_count = results['status_distribution']['counts'].get('Implemented', 0)
    results['metadata']['implementation_rate'] = round(impl_count / len(df) * 100, 2)
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON results
        with open(output_path / 'analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to {output_path / 'analysis_results.json'}")
    
    return results


def print_summary(results: dict):
    """Print a summary of the analysis results."""
    meta = results['metadata']
    status = results['status_distribution']
    
    print("\n" + "="*60)
    print("ACC FORUM ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\nTotal Ideas: {meta['total_ideas']:,}")
    print(f"Date Range: {meta['date_range']['start']} to {meta['date_range']['end']}")
    print(f"Total Kudos: {meta['total_kudos']:,}")
    print(f"Total Views: {meta['total_views']:,}")
    print(f"Implementation Rate: {meta['implementation_rate']}%")
    
    print("\nStatus Distribution:")
    for status_name, count in status['counts'].items():
        pct = status['percentages'][status_name]
        print(f"  {status_name}: {count} ({pct}%)")
    
    print("\nTop Categories by Kudos:")
    sorted_cats = sorted(results['categories'].items(), 
                        key=lambda x: x[1]['kudos'], reverse=True)[:5]
    for cat, stats in sorted_cats:
        print(f"  {cat}: {stats['kudos']:,} kudos ({stats['count']} ideas)")
    
    print("\nTop Pain Patterns:")
    sorted_patterns = sorted(results['pain_patterns'].items(),
                            key=lambda x: x[1]['kudos'], reverse=True)[:5]
    for pattern, stats in sorted_patterns:
        print(f"  {pattern}: {stats['kudos']:,} kudos ({stats['count']} ideas)")
    
    print("\nTop 5 Most-Voted Ideas:")
    for i, idea in enumerate(results['top_ideas'][:5], 1):
        print(f"  {i}. [{idea['kudos']} kudos] {idea['title'][:50]}...")
        print(f"     Status: {idea['status_name']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze ACC Forum Ideas')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output directory for results')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress summary output')
    
    args = parser.parse_args()
    
    results = run_full_analysis(args.input, args.output)
    
    if not args.quiet:
        print_summary(results)

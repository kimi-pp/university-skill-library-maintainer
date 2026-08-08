#!/usr/bin/env python3
"""
Test the thesis review with the sample thesis that has intentional issues.
"""

import sys
import os
from datetime import datetime

# Add current directory to path to import thesis_review
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thesis_review import ThesisReviewer

def test_with_sample_thesis():
    """Test with the sample thesis that has intentional issues."""
    input_path = "test_files/thesis_sample.docx"
    output_dir = "thesis-review-workspace/iteration-1/eval-comprehensive-review/with_skill/outputs/"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"sample_thesis_review_{timestamp}.docx")

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"错误: 输入文件不存在: {input_path}")
        print("请先运行 generate_test_docx.py 生成测试文件")
        return

    try:
        # Initialize reviewer
        reviewer = ThesisReviewer(input_path)

        # Perform review
        reviewer.perform_comprehensive_review()

        # Generate review document
        review_doc = reviewer.generate_review_document(output_path)

        print("\n" + "="*60)
        print("样本论文评审完成!")
        print(f"输入文件: {input_path}")
        print(f"输出文件: {output_path}")
        print(f"发现问题: {len(reviewer.issues)}个")
        print("="*60)

        # Print detailed summary
        if reviewer.issues:
            print("\n按类别统计:")
            categories = {}
            for issue in reviewer.issues:
                cat = issue['category']
                categories[cat] = categories.get(cat, 0) + 1

            for cat, count in categories.items():
                print(f"  {cat}: {count}个问题")

            print("\n高优先级问题:")
            high_issues = [i for i in reviewer.issues if i['priority'] == 'high']
            for issue in high_issues[:5]:
                print(f"  - {issue['description']} ({issue['location']})")

            print("\n中优先级问题 (示例):")
            medium_issues = [i for i in reviewer.issues if i['priority'] == 'medium']
            for issue in medium_issues[:3]:
                print(f"  - {issue['description']} ({issue['location']})")

        if reviewer.positive_feedback:
            print("\n做得好的方面:")
            for feedback in reviewer.positive_feedback:
                print(f"  - {feedback}")

    except Exception as e:
        print(f"评审过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_with_sample_thesis()
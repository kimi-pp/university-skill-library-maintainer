#!/usr/bin/env python3
"""
运行论文评审的脚本
"""

import os
import sys
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入评审类
from thesis_review_txt import ThesisReviewer

def main():
    """主函数"""
    # 输入和输出路径
    input_path = "test_files/论文终稿.docx"
    output_dir = "thesis-review-workspace/iteration-2/eval-focused-check/with_skill/outputs/"

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"论文终稿_评审意见_{timestamp}.txt")

    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    try:
        # 初始化评审器
        print(f"开始评审: {input_path}")
        reviewer = ThesisReviewer(input_path)

        # 执行评审
        reviewer.perform_comprehensive_review()

        # 生成评审文档
        review_doc = reviewer.generate_review_text(output_path)

        print("\n" + "="*60)
        print("论文评审完成!")
        print(f"输入文件: {input_path}")
        print(f"输出文件: {output_path}")
        print(f"发现问题: {len(reviewer.issues)}个")
        print("="*60)

        # 打印摘要
        if reviewer.issues:
            print("\n主要问题摘要:")
            high_issues = [i for i in reviewer.issues if i['priority'] == 'high']
            if high_issues:
                print("高优先级问题:")
                for issue in high_issues[:3]:
                    print(f"  - {issue['description']} ({issue['location']})")

            if reviewer.positive_feedback:
                print("\n做得好的方面:")
                for feedback in reviewer.positive_feedback:
                    print(f"  - {feedback}")

    except Exception as e:
        print(f"评审过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
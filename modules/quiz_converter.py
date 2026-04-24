"""
CourseForge Quiz Converter
将 Markdown 格式的场景化通关测试转换为 LMS 导入所需的 JSON 结构
"""

import re
from typing import List, Dict


class QuizConverter:
    """将 scenario_quiz.md 格式的 Markdown 解析为结构化 JSON 题目列表"""

    @staticmethod
    def parse_markdown_quiz(md_text: str) -> List[Dict]:
        """
        解析 Markdown 格式的场景化通关测试。
        支持极简格式：
        1. [章节][小节] 问题描述？
        A. 选项1
        B. 选项2
        C. 选项3
        D. 选项4
        答案：B
        """
        if not md_text or not md_text.strip():
            return []

        questions = []
        current_type = "单选题"
        lines = md_text.strip().split('\n')
        current_q = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("#### ") or line.startswith("### "):
                if "多选题" in line:
                    current_type = "多选题"
                elif "单选题" in line:
                    current_type = "单选题"
                elif "判断题" in line:
                    current_type = "判断题"
                elif "填空题" in line:
                    current_type = "填空题"
                continue

            # Match question start: "1. [xxx][yyy] text..." or "1. text..."
            # 兼容 Markdown 列表如 "* 1." 或 "1."
            clean_line = re.sub(r'^[\*\-]\s*', '', line)
            q_match = re.match(r'^(\d+)[\.\、\:]\s*(?:\[(.*?)\]\[(.*?)\])?\s*(.*)', clean_line)
            
            if q_match:
                if current_q:
                    # Save previous question
                    questions.append(current_q)
                    
                chapter = q_match.group(2).strip() if q_match.group(2) else ""
                section = q_match.group(3).strip() if q_match.group(3) else ""
                q_text = q_match.group(4).strip()
                
                # 若形如 **问题**：xxx，去掉干扰前缀
                q_text = re.sub(r'^\*\*(?:问题|题目|场景)\*\*[：:]\s*', '', q_text)
                
                current_q = {
                    "chapter": chapter,
                    "section": section,
                    "question": q_text,
                    "type": current_type,
                    "options": [],
                    "answer_content": "",
                    "analysis": ""
                }
                continue

            if current_q:
                # 解析选项
                if current_type in ["单选题", "多选题"]:
                    # 匹配 "A. xxx" 或 "* A. xxx"
                    opt_line = re.sub(r'^[\*\-]\s*', '', line)
                    opt_match = re.match(r'^([A-Z])[\.\、\:\s]\s*(.*)', opt_line)
                    if opt_match:
                        # 原样保留 A. xxx 格式作为 text 供后续导出或二次处理
                        current_q["options"].append({
                            "letter": opt_match.group(1),
                            "text": opt_line,
                            "is_correct": False
                        })
                        continue

                # 解析答案
                clean_ans_line = re.sub(r'^\*\*(?:正确答案|答案)\*\*[：:]\s*', '答案：', line)
                ans_match = re.match(r'^答案[：:]\s*(.*)', clean_ans_line)
                if ans_match:
                    ans_val = ans_match.group(1).strip()
                    if current_type in ["单选题", "多选题"]:
                        correct_letters = [c for c in ans_val if c in 'ABCD']
                        for opt in current_q["options"]:
                            if opt.get("letter") in correct_letters:
                                opt["is_correct"] = True
                    elif current_type == "判断题":
                         # 兼容 对/错/是/否/T/F
                         current_q["answer_content"] = "是" if ans_val in ["是", "对", "正确", "T", "True"] else "否"
                    elif current_type == "填空题":
                         current_q["answer_content"] = ans_val
                    continue
                
                # 解析解析
                analysis_match = re.search(r'^\*\*(?:深度解析|解析)\*\*[：:]\s*(.*)', line)
                if analysis_match:
                    current_q["analysis"] = analysis_match.group(1).strip()
                    continue
                elif line.startswith("解析：") or line.startswith("深度解析："):
                    current_q["analysis"] = re.sub(r'^(?:深度解析|解析)[：:]\s*', '', line).strip()
                    continue

        if current_q:
            questions.append(current_q)

        # 整理输出并清理辅助字段
        for i, q in enumerate(questions):
            q['seq'] = i + 1
            if "options" in q:
                for opt in q["options"]:
                    opt.pop("letter", None)

        return questions

    @staticmethod
    def parse_lms_mixed_response(text: str) -> List[Dict]:
        """
        解析 LMS 混合响应（Markdown + JSON 双轨输出）。
        优先从 JSON 代码块提取，如果 JSON 被截断，则回退到 Markdown 解析。
        """
        import json
        
        # 1. 先尝试提取完整的 JSON 代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                pass
        
        # 2. JSON 代码块可能被截断（无 ``` 结尾），尝试提取并修复
        json_start = re.search(r'```json\s*', text)
        if json_start:
            json_fragment = text[json_start.end():].strip()
            repaired = QuizConverter._repair_truncated_json(json_fragment)
            if repaired:
                return repaired
        
        # 3. 尝试匹配裸 JSON 数组
        bracket_match = re.search(r'\[\s*\{', text)
        if bracket_match:
            json_fragment = text[bracket_match.start():]
            try:
                return json.loads(json_fragment)
            except json.JSONDecodeError:
                repaired = QuizConverter._repair_truncated_json(json_fragment)
                if repaired:
                    return repaired
        
        # 4. 最终回退：用 Markdown 解析器
        return QuizConverter.parse_markdown_quiz(text)

    @staticmethod
    def _repair_truncated_json(fragment: str) -> List[Dict]:
        """
        尝试修复被截断的 JSON 数组。
        策略：逐个提取已完成的 JSON 对象。
        """
        import json
        
        results = []
        depth = 0
        start = None
        
        for i, ch in enumerate(fragment):
            if ch == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0 and start is not None:
                    obj_str = fragment[start:i+1]
                    try:
                        obj = json.loads(obj_str)
                        if isinstance(obj, dict) and 'question' in obj:
                            results.append(obj)
                    except json.JSONDecodeError:
                        pass
                    start = None
        
        return results

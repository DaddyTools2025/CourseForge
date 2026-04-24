"""
CourseForge AI Generator
基于 OpenAI Compatible API 的内容生成引擎
支持内部 AI 平台 (appkey) 和外网 (Google GenAI / Anthropic SDK) 双模式
"""

import re
from typing import Optional, Dict, Any
import traceback
import time
import random
import requests
import anthropic
from anthropic import Anthropic
import google.generativeai as genai
from openai import OpenAI
from .prompts import PromptTemplates, get_system_prompt
from .logger import VibeLogger


class AIGenerator:
    """AI 内容生成器"""

    def __init__(self, api_key: str, base_url: str, model_name: str = "gemini-2.5-pro", 
                 custom_system_prompt: str = None, api_mode: str = 'external', appkey: str = None, industry: str = "通用企业"):
        """
        初始化 AI 生成器

        Args:
            api_key: API 密钥（外网模式）
            base_url: API 基础 URL
            model_name: 模型名称
            custom_system_prompt: 自定义系统 Prompt（可选，默认使用专业模板）
            api_mode: API 模式 - 'internal'（内部 AI 平台）或 'external'（外网）
            appkey: 内部平台应用标识（内网模式）
        """
        self.model_name = model_name
        self.prompts = PromptTemplates()
        self.industry = industry
        self.system_prompt = custom_system_prompt or get_system_prompt(self.industry)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/') if base_url else ""
        self.api_mode = api_mode
        self.appkey = appkey

        if self.api_mode == 'internal':
            # 内网模式：使用 requests 直接调用，无需初始化 SDK
            VibeLogger.info(f"Initializing internal AI mode: model={model_name}, url={base_url}")
        else:
            # 判断使用的 SDK/协议 模式
            self.use_anthropic_sdk = False
            self.use_google_rest = False
            self.anthropic_client = None
            
            # 1. 直连 Google API Key 模式 (使用 requests 构建 Gemini REST 调用)
            # Google API Key 通常以 AIza 开头，或者 base_url 没填，或者填了 googleapis
            if self.base_url == "" or "googleapis.com" in self.base_url or (self.api_key and self.api_key.startswith("AIza")):
                self.use_google_rest = True
                if not self.base_url:
                    self.base_url = "https://generativelanguage.googleapis.com"
                VibeLogger.info(f"Initializing Google REST Mode: model={model_name}")
            else:
                # 2. Antigravity 代理模式 (使用 Anthropic SDK 兼容任意模型)
                self.use_anthropic_sdk = True
                VibeLogger.info(f"Initializing Antigravity (Anthropic SDK) Mode: model={model_name}, url={self.base_url}")
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(
                    api_key=self.api_key or "YOUR_API_KEY_HERE", # Anthropic SDK 需要 api_key 不能空
                    base_url=self.base_url
                )

    def _call_internal_api(
        self,
        prompt: str,
        system_message: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        内部 AI 平台 API 调用
        使用 appkey Header 鉴权，直接 HTTP POST 请求
        """
        final_system_message = system_message or self.system_prompt
        
        headers = {
            "Content-Type": "application/json",
            "appkey": self.appkey  # 注意：Header 字段名必须是小写 appkey
        }
        
        body = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": final_system_message},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "temperature": temperature
        }
        
        VibeLogger.debug(f"Internal AI request: url={self.base_url}, model={self.model_name}, temp={temperature}")
        VibeLogger.debug(f"Prompt preview (len={len(prompt)}): {prompt[:100]}...")
        
        resp = requests.post(
            self.base_url,
            headers=headers,
            json=body,
            timeout=180  # 长文本生成可能耗时较长
        )
        
        # 检查 HTTP 状态码
        if resp.status_code != 200:
            error_detail = ""
            try:
                error_detail = resp.text[:500]
            except Exception:
                pass
            raise RuntimeError(f"内部 AI API 返回错误 (HTTP {resp.status_code}): {error_detail}")
        
        data = resp.json()
        
        # 解析 OpenAI-compatible 响应格式
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0].get("message", {}).get("content", "")
            if content:
                VibeLogger.debug(f"Internal AI response received, length={len(content)}")
                return content.strip()
            else:
                raise RuntimeError(f"内部 AI API 返回了空内容: {data}")
        else:
            raise RuntimeError(f"内部 AI API 响应格式异常: {data}")

    def _call_ai(
        self,
        prompt: str,
        system_message: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        max_retries: int = 3,
        strip_thinking: bool = True,
        image_data: str = None
    ) -> str:
        """
        调用 AI API (支持重试和思维链清洗)
        """
        last_error = None
        result = ""

        for attempt in range(max_retries + 1):
            try:
                final_system_message = system_message or self.system_prompt

                VibeLogger.debug(f"Calling AI (Attempt {attempt+1}/{max_retries+1}): url={self.base_url}, model={self.model_name}, temp={temperature}")
                VibeLogger.debug(f"Prompt preview (len={len(prompt)}): {prompt[:100]}...")

                if self.api_mode == 'internal':
                    # --- 内网平台 Path ---
                    result = self._call_internal_api(prompt, system_message, temperature, max_tokens)
                    
                elif self.use_anthropic_sdk:
                    # --- Antigravity 代理模式: 透传任意模型，采用 Anthropic SDK 协议 ---
                    import anthropic
                    content_list = [{"type": "text", "text": prompt}]
                    if image_data:
                        content_list.insert(0, {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}
                        })
                    kwargs = {
                        "model": self.model_name,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "messages": [{"role": "user", "content": content_list}]
                    }
                    if final_system_message:
                        kwargs["system"] = final_system_message
                        
                    try:
                        response = self.anthropic_client.messages.create(**kwargs)
                        result = response.content[0].text.strip()
                    except Exception as e:
                        # 对于 Anthropic SDK 提取 error body
                        error_body = ""
                        if hasattr(e, 'response') and hasattr(e.response, 'text'):
                            error_body = str(e.response.text)
                        raise RuntimeError(f"Antigravity/Anthropic 代理返回错误:\n{str(e)}\n{error_body}")
                        
                elif self.use_google_rest:
                    # --- 直连 Google API 模式 ---
                    base = self.base_url
                    if "v1beta" not in base and "generateContent" not in base:
                        req_url = f"{base}/v1beta/models/{self.model_name}:generateContent"
                    else:
                        req_url = base

                    if "?" in req_url:
                        req_url += f"&key={self.api_key}"
                    else:
                        req_url += f"?key={self.api_key}"

                    headers = {"Content-Type": "application/json"}
                    parts = [{"text": prompt}]
                    if image_data:
                        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_data}})
                    payload = {
                        "contents": [{"parts": parts}],
                        "generationConfig": {
                            "temperature": temperature,
                            "maxOutputTokens": max_tokens
                        }
                    }
                    if final_system_message:
                        payload["systemInstruction"] = {"parts": [{"text": final_system_message}]}

                    try:
                        resp = requests.post(req_url, headers=headers, json=payload, timeout=180)
                    except requests.exceptions.RequestException as req_e:
                        raise RuntimeError(f"网络连接失败 ({self.base_url}): {str(req_e)}")

                    if resp.status_code != 200:
                        raise RuntimeError(f"Google API 服务拒绝请求 (HTTP {resp.status_code}):\n{resp.text}")

                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if not candidates:
                        raise RuntimeError(f"API 响应中没有候选内容: {data}")
                        
                    content_parts = candidates[0].get("content", {}).get("parts", [])
                    if not content_parts:
                        raise RuntimeError(f"候选内容为空: {data}")
                        
                    result = content_parts[0].get("text", "").strip()

                # 统一后处理：思维链清洗
                if strip_thinking:
                    return self._strip_thinking_content(result)
                return result

            except Exception as e:
                error_str = str(e)
                last_error = e

                # Check for retryable errors (429, 503, Resource Exhausted)
                is_retryable = False
                if "429" in error_str or "503" in error_str or "ResourceExhausted" in error_str or "capacity available" in error_str:
                    is_retryable = True

                VibeLogger.error(f"AI Call Attempt {attempt+1} failed: {error_str}")

                if is_retryable and attempt < max_retries:
                    sleep_time = (2 ** attempt) + random.uniform(0, 1) # Exponential backoff
                    VibeLogger.warning(f"Retryable error detected. Sleeping for {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    continue

                raise RuntimeError(f"AI 调用失败: {error_str}")

    @staticmethod
    def _strip_thinking_content(text: str) -> str:
        """
        去除 AI 响应中的思维链（thinking chain）内容。
        
        部分内部 CoT 模型（如深度推理模型）会将英文推理过程直接
        拼入 content 字段，导致输出前半段出现大量英文分析段落。
        本方法检测并截取第一个中文 Markdown 标题之后的实际内容。
        """
        if not text:
            return text

        # 1. 处理 <think>...</think> 标签（部分模型会用此标签包裹推理）
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        if not cleaned:
            cleaned = text  # 如果全部被移除，回退原文

        # 安全检查：如果内容看起来像 JSON 或代码块，跳过基于 Markdown 标题的清洗
        # 避免误伤 PPT 大纲等 JSON 输出
        if "```json" in cleaned or cleaned.startswith("{"):
            return cleaned

        # 2. 查找第一个中文 Markdown 标题行（## 开头且包含中文字符）
        lines = cleaned.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('## ') and re.search(r'[\u4e00-\u9fff]', stripped):
                # 找到了正式内容的起点，截取此行及之后的内容
                result = '\n'.join(lines[i:])
                VibeLogger.debug(f"Stripped {i} lines of thinking chain content")
                return result.strip()

        # 3. 没有找到明确切分点，返回清洗后的内容
        return cleaned

    @staticmethod
    def extract_json_from_response(text: str) -> list:
        """从 AI 响应中提取 JSON 数组并进行容错处理（支持截断修复 + Markdown 回退）"""
        if not text:
            return []
            
        try:
            from .quiz_converter import QuizConverter
            return QuizConverter.parse_lms_mixed_response(text)
        except Exception as e:
            VibeLogger.error(f"提取 JSON 失败: {e}\nRaw text: {text[:500]}")
            return []


    def extract_slide_knowledge(self, text: str, image_blob: bytes = None) -> dict:
        """
        多模态/OCR 兜底萃取单页内容，用于后续写入 PPT 备注。
        无视字数，只要有图必走多模态。强制返回两段式结构防自由发挥。
        """
        prompt = """
        请提取以下 PPT 页面的核心信息。
        
        【任务 1：智能标题提取极其净素化】
        观察页面最顶部。如果存在类似『提示词工程 - 提示词概念及类型』或『01 传统金融与数字金融』的标题栏，请智能拆分它。破折号/空格前的部分作为 `chapter`，后面的部分作为 `section`。若无法清晰拆分，则直接归入 `chapter`。
        **名称净素化规则**：绝对禁止在 `chapter` 和 `section` 的取值中保留“第一章”、“第一部分”、“1.1”、“01”等任何数字或结构层级前缀！只截取纯文本名称（例如“01 传统”应变为“传统”）。
        
        【任务 2：生成双层结构的讲师备注 (最高优先级)】
        为了防止原文丢失，你生成的 `knowledge_base` 文本必须严格遵循以下“两段式”结构，不允许有任何自行发挥的开头或结尾：

        第一段：【页面原文】
        (你必须像打字员一样，把图片或提供的文本中的所有文字一字不落地抄写下来，包括所有的标题、列表、图表内的数据标签，绝不遗漏和润色)

        第二段：【讲师解读】
        (在这里发挥你的大模型优势，结合你看到的原文，为讲师生成一段用于口头演说的连贯讲解词，解释概念并指出重点)
        
        【输入素材】
        页面文本参考（可能不全）：
        {text_content}
        
        必须严格输出以下JSON格式（注意双括号）：
        ```json
        {{
          "chapter": "提取的章节名称(若无则推论或留空)",
          "section": "提取的小节名称(若无则推论或留空)",
          "knowledge_base": "【页面原文】\\n...\\n\\n【讲师解读】\\n..."
        }}
        ```
        """
        formatted_prompt = prompt.format(text_content=text if text else "无明显文本(重点依赖读图)")
        
        try:
            # 无论字数多少，只要图片存在，就传递图片和文本一并给大模型（假设底座_call_ai支持image_data参数）
            # 注意目前的_call_ai设计可能受制于底座库传入能力。如果是Gemini或Anthropic，这里应该传入Base64。
            # 这里按照原架构保留_call_ai接口调用，但移除字数拦截逻辑。
            import base64
            image_data = None
            if image_blob:
                image_data = base64.b64encode(image_blob).decode('utf-8')
            
            response = self._call_ai(formatted_prompt, image_data=image_data, strip_thinking=True)
            
            # 使用自带的JSON提取方法
            questions = self.extract_json_from_response(response)
            if questions and isinstance(questions, list) and len(questions) > 0:
                 return questions[0]
            elif questions and isinstance(questions, dict):
                 return questions
            else:
                 return {
                     "chapter": "待补充",
                     "section": "待补充",
                     "knowledge_base": response
                 }
                 
        except Exception as e:
            # 异常防御兜底
            import logging
            logging.error(f"提取 PPT 备注异常: {e}")
            return {
                "chapter": "待补充",
                "section": "待补充",
                "knowledge_base": f"AI提炼失败：{e}"
            }

    def extract_core_content(self, course_content: str, audience_level: str) -> str:
        """
        提取课件核心内容
        
        Args:
            course_content: 原始课件文本
            audience_level: 受众级别
            
        Returns:
            结构化的核心内容
        """
        prompt = self.prompts.get_content_extraction_prompt(audience_level)
        full_prompt = f"{prompt}\n\n**原始课件内容**:\n{course_content}"
        
        raw_result = self._call_ai(
            full_prompt,
            temperature=0.3,  # 提取内容需要更准确
            max_tokens=3000
        )
        
        # _call_ai 内部已包含 _strip_thinking_content，此处直接返回
        return raw_result
    
    def generate_video_script(self, core_content: str, audience_level: str) -> str:
        """
        生成视频旁白脚本
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            视频脚本
        """
        prompt = self.prompts.get_video_script_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.8,  # 创作性内容可以更有创意
            max_tokens=4000
        )
    
    def generate_interactions(self, core_content: str, audience_level: str) -> str:
        """
        生成课堂互动方案
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            互动方案
        """
        prompt = self.prompts.get_interaction_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.7,
            max_tokens=3000
        )
    
    def generate_action_plan(self, core_content: str, audience_level: str) -> str:
        """
        生成回岗实践计划
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            行动计划
        """
        prompt = self.prompts.get_action_plan_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.6,  # 需要务实可行
            max_tokens=3000
        )
    
    def generate_surveys(self, core_content: str, audience_level: str) -> str:
        """
        生成双向调研问卷
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            调研问卷
        """
        prompt = self.prompts.get_survey_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.5,  # 问卷需要规范性
            max_tokens=3000
        )
    
    def generate_ppt_outline(self, core_content: str, audience_level: str) -> str:
        """
        生成 PPT 大纲（JSON 格式）
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            JSON 格式的 PPT 大纲
        """
        prompt = self.prompts.get_ppt_outline_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.4,  # 结构化内容需要精确
            max_tokens=4000
        )

    def generate_precourse_outline(self, core_content: str, audience_level: str) -> str:
        """
        生成先导课程大纲（3-5分钟微课）
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            
        Returns:
            先导微课大纲
        """
        prompt = self.prompts.get_precourse_outline_prompt(core_content, audience_level)
        
        return self._call_ai(
            prompt,
            temperature=0.7,  # 案例创作需要一定创意
            max_tokens=3000
        )

    def generate_scenario_quiz(self, core_content: str, audience_level: str, course_name: str = "") -> dict:
        """
        生成场景化通关测试（20道单选题）
        
        Args:
            core_content: 核心内容
            audience_level: 受众级别
            course_name: 课程名称
            
        Returns:
            场景化通关测试题目字典 {'markdown': ..., 'json_data': ...}
        """
        prompt = self.prompts.get_scenario_quiz_prompt(core_content, audience_level, course_name=course_name, industry=self.industry)
        
        response = self._call_ai(
            prompt,
            temperature=0.6,  # 平衡创意与准确性
            max_tokens=8192   # 10题/小节配额需要极大 token
        )
        
        json_data = self.extract_json_from_response(response)
        
        return {
            "markdown": response,
            "json_data": json_data
        }

    def generate_all_materials(
        self, 
        course_content: str, 
        audience_level: str,
        options: Dict[str, bool] = None,
        progress_callback: Optional[callable] = None,
        course_name: str = ""
    ) -> Dict[str, Any]:
        """
        一键生成所有教学材料
        
        Args:
            course_content: 原始课件内容
            audience_level: 受众级别
            options: 生成选项开关 {'video_script': True, ...}
            progress_callback: 进度回调函数 (step_name: str, progress: float)
            
        Returns:
            包含所有生成内容的字典
        """
        results = {}
        
        # 默认全部生成
        if options is None:
            options = {}
        
        def is_enabled(key):
            return options.get(key, True)
            
        # 计算总步骤数 (核心内容总是+1)
        steps = ['core_content']
        if is_enabled('precourse_outline'): steps.append('precourse_outline')
        if is_enabled('video_script'): steps.append('video_script')
        if is_enabled('interactions'): steps.append('interactions')
        if is_enabled('action_plan'): steps.append('action_plan')
        if is_enabled('surveys'): steps.append('surveys')
        if is_enabled('scenario_quiz'): steps.append('scenario_quiz')
        if is_enabled('ppt_outline'): steps.append('ppt_outline')
        
        total_steps = len(steps)
        current_step = 0
        
        def update_step(msg):
            nonlocal current_step
            current_step += 1
            if progress_callback:
                progress_callback(msg, current_step / total_steps)

        # 步骤 1: 提取核心内容 (Always run)
        update_step("正在提取核心内容...")
        results['core_content'] = self.extract_core_content(course_content, audience_level)
        
        # 步骤 2: 先导课程大纲
        if is_enabled('precourse_outline'):
            update_step("正在生成先导课程大纲...")
            results['precourse_outline'] = self.generate_precourse_outline(results['core_content'], audience_level)
        
        # 步骤 3: 视频脚本
        if is_enabled('video_script'):
            update_step("正在生成视频旁白脚本...")
            results['video_script'] = self.generate_video_script(results['core_content'], audience_level)
        
        # 步骤 4: 互动方案
        if is_enabled('interactions'):
            update_step("正在设计课堂互动...")
            results['interactions'] = self.generate_interactions(results['core_content'], audience_level)
        
        # 步骤 5: 行动计划
        if is_enabled('action_plan'):
            update_step("正在制定回岗实践计划...")
            results['action_plan'] = self.generate_action_plan(results['core_content'], audience_level)
        
        # 步骤 6: 调研问卷
        if is_enabled('surveys'):
            update_step("正在设计调研问卷...")
            results['surveys'] = self.generate_surveys(results['core_content'], audience_level)
        
        # 步骤 7: 场景化通关测试
        if is_enabled('scenario_quiz'):
            update_step("正在生成场景化通关测试...")
            results['scenario_quiz'] = self.generate_scenario_quiz(results['core_content'], audience_level, course_name=course_name)
        
        # 步骤 8: PPT 大纲
        if is_enabled('ppt_outline'):
            update_step("正在生成 PPT 大纲...")
            results['ppt_outline'] = self.generate_ppt_outline(results['core_content'], audience_level)
        
        return results


# 便捷函数
def create_generator(api_key: str, base_url: str, model_name: str = "gemini-2.5-pro", 
                     custom_system_prompt: str = None, api_mode: str = 'external', appkey: str = None, industry: str = "通用企业") -> AIGenerator:
    """创建 AI 生成器实例"""
    return AIGenerator(api_key, base_url, model_name, custom_system_prompt, api_mode, appkey, industry)

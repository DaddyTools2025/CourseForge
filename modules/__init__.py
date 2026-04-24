"""
CourseForge Modules
核心功能模块集合
"""

from .file_parser import FileParser, extract_text_from_file
from .ai_generator import AIGenerator, create_generator
from .ppt_builder import (
    PPTBuilder, generate_ppt_from_outline,
    save_template, delete_template, get_saved_template_path
)
from .prompts import PromptTemplates, get_system_prompt
from .config_manager import ConfigManager, load_or_create_config, is_configured

__all__ = [
    'FileParser',
    'extract_text_from_file',
    'AIGenerator',
    'create_generator',
    'PPTBuilder',
    'generate_ppt_from_outline',
    'save_template',
    'delete_template',
    'get_saved_template_path',
    'PromptTemplates',
    'get_system_prompt',
    'ConfigManager',
    'load_or_create_config',
    'is_configured'
]


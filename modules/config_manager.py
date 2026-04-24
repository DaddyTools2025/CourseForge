"""
CourseForge Configuration Manager
配置文件管理模块
"""

import os
import json
from typing import Optional, Dict
from pathlib import Path


class ConfigManager:
    """配置管理器"""
    
    CONFIG_FILE = "courseforge_config.json"
    
    @staticmethod
    def get_config_path() -> Path:
        """获取配置文件路径"""
        # 优先使用用户主目录
        config_dir = Path.home() / ".courseforge"
        config_dir.mkdir(exist_ok=True)
        return config_dir / ConfigManager.CONFIG_FILE
    
    @staticmethod
    def load_config() -> Optional[Dict]:
        """
        加载配置文件
        
        Returns:
            配置字典，如果不存在则返回 None
        """
        config_path = ConfigManager.get_config_path()
        
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"配置加载失败: {e}")
            return None
    
    @staticmethod
    def save_config(config: Dict) -> bool:
        """
        保存配置文件
        
        Args:
            config: 配置字典
            
        Returns:
            是否保存成功
        """
        config_path = ConfigManager.get_config_path()
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"配置保存失败: {e}")
            return False
    
    @staticmethod
    def delete_config() -> bool:
        """
        删除配置文件
        
        Returns:
            是否删除成功
        """
        config_path = ConfigManager.get_config_path()
        
        try:
            if config_path.exists():
                config_path.unlink()
            return True
        except Exception as e:
            print(f"配置删除失败: {e}")
            return False
    
    @staticmethod
    def validate_config(config: Dict) -> tuple[bool, str]:
        """
        验证配置是否有效
        
        Args:
            config: 配置字典
            
        Returns:
            (是否有效, 错误消息)
        """
        api_mode = config.get('api_mode', 'external')
        
        if api_mode == 'internal':
            # 内网模式：需要 appkey + internal_url + internal_model
            if not config.get('appkey'):
                return False, "内网模式下 appkey（应用标识）不能为空"
            if not config.get('internal_url'):
                return False, "内网模式下接口地址不能为空"
            if not config.get('internal_url', '').startswith('http'):
                return False, "接口地址格式不正确（应以 http:// 或 https:// 开头）"
            if not config.get('internal_model'):
                return False, "内网模式下必须选择模型通道"
        else:
            # 外网模式：需要 api_key + model_name
            required_fields = ['api_key', 'model_name']
            for field in required_fields:
                if field not in config or not config[field]:
                    return False, f"缺少必需字段: {field}"
            
            if not config['api_key']:
                return False, "API Key 不能为空"
            if config.get('base_url') and not config['base_url'].startswith('http'):
                return False, "Base URL 格式不正确（应以 http:// 或 https:// 开头）"
        
        return True, ""
    
    @staticmethod
    def get_default_config() -> Dict:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            'api_mode': 'external',           # 'internal' | 'external'
            'api_key': '',
            'base_url': '',
            'model_name': 'gemini-2.5-pro',
            'custom_system_prompt': '',
            'appkey': '',                      # 内部 AI 平台 appkey（应用标识）
            'internal_url': '',                # 内部 AI 平台接口地址
            'internal_model': 'internal-model-fast'      # 内部模型通道编码
        }


# 便捷函数
def load_or_create_config() -> Dict:
    """
    加载配置或创建默认配置
    
    Returns:
        配置字典
    """
    config = ConfigManager.load_config()
    if config is None:
        config = ConfigManager.get_default_config()
    return config


def is_configured() -> bool:
    """
    检查是否已配置
    
    Returns:
        是否已配置
    """
    config = ConfigManager.load_config()
    if config is None:
        return False
    
    is_valid, _ = ConfigManager.validate_config(config)
    return is_valid

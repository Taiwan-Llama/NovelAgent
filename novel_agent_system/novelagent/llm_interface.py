"""
LLM接口模組 - 提供與語言模型的交互功能
"""

from typing import Dict, Any, List, Optional, Union
import litellm


class LLMInterface:
    """
    LLM接口，提供與語言模型的交互功能
    
    屬性:
        config (Dict[str, Any]): 配置信息
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化LLM接口
        
        參數:
            config (Dict[str, Any]): 配置信息
        """
        self.config = config
        
        # 設置LiteLLM配置
        if "api_key" in config:
            litellm.api_key = config["api_key"]
        
        if "api_base" in config:
            litellm.api_base = config["api_base"]
    
    def generate(self, prompt: str, system_message: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        生成文本
        
        參數:
            prompt (str): 提示
            system_message (Optional[str]): 系統消息
            temperature (float): 溫度參數
            
        返回:
            str: 生成的文本
        """
        try:
            response = litellm.completion(
                model=self.config.get("model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_message or "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=self.config.get("max_tokens", 1000)
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Error generating text: {e}"
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        聊天模式
        
        參數:
            messages (List[Dict[str, str]]): 消息列表
            temperature (float): 溫度參數
            
        返回:
            str: 生成的回應
        """
        try:
            response = litellm.completion(
                model=self.config.get("model", "gpt-3.5-turbo"),
                messages=messages,
                temperature=temperature,
                max_tokens=self.config.get("max_tokens", 1000)
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in chat: {e}")
            return f"Error in chat: {e}"
    
    def stream_generate(self, prompt: str, system_message: Optional[str] = None, temperature: float = 0.7):
        """
        流式生成文本
        
        參數:
            prompt (str): 提示
            system_message (Optional[str]): 系統消息
            temperature (float): 溫度參數
            
        返回:
            generator: 生成的文本流
        """
        try:
            response = litellm.completion(
                model=self.config.get("model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_message or "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=self.config.get("max_tokens", 1000),
                stream=True
            )
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error in stream generate: {e}")
            yield f"Error in stream generate: {e}"
    
    def get_embedding(self, text: str) -> List[float]:
        """
        獲取文本的嵌入向量
        
        參數:
            text (str): 文本
            
        返回:
            List[float]: 嵌入向量
        """
        try:
            response = litellm.embedding(
                model=self.config.get("embedding_model", "text-embedding-ada-002"),
                input=text
            )
            
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # 返回零向量作為後備
            return [0.0] * 1536  # 默認維度

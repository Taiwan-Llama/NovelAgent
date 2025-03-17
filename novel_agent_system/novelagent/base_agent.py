"""
基礎代理類模組 - 提供所有代理的基礎功能
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from .memory import Memory
from .llm_interface import LLMInterface


@dataclass
class Action:
    """代理行動的數據類"""
    tool: str
    args: Dict[str, Any]
    thought: str = ""


class BaseAgent:
    """
    基礎代理類，提供所有代理的通用功能
    
    屬性:
        name (str): 代理名稱
        role (str): 代理角色
        llm (LLMInterface): 語言模型接口
        memory (Memory): 記憶系統
        tools (Dict[str, Callable]): 可用工具
    """
    
    def __init__(self, name: str, role: str, llm_config: Dict[str, Any]):
        """
        初始化基礎代理
        
        參數:
            name (str): 代理名稱
            role (str): 代理角色
            llm_config (Dict[str, Any]): 語言模型配置
        """
        self.name = name
        self.role = role
        self.llm = LLMInterface(llm_config)
        self.memory = Memory()
        self.tools = {}
        self.system_prompt = f"You are {name}, a {role}."
    
    def think(self, context: str) -> str:
        """
        思考過程，可以被子類重寫
        
        參數:
            context (str): 上下文信息
            
        返回:
            str: 思考結果
        """
        # 獲取相關記憶
        relevant_memories = self.memory.search(context)
        
        # 構建提示
        prompt = f"""
        Based on the following context and your relevant memories, what should you do next?
        
        Context:
        {context}
        
        Relevant Memories:
        {relevant_memories}
        
        Think step by step about what to do next.
        """
        
        # 生成思考
        thought = self.llm.generate(prompt, self.system_prompt)
        
        # 記錄思考
        self.memory.add({"type": "thought", "content": thought})
        
        return thought
    
    def act(self, thought: str) -> Action:
        """
        行動過程，可以被子類重寫
        
        參數:
            thought (str): 思考結果
            
        返回:
            Action: 行動
        """
        # 構建提示
        tools_description = "\n".join([f"- {name}: {func.__doc__}" for name, func in self.tools.items()])
        
        prompt = f"""
        Based on your thought, decide which tool to use and with what arguments.
        
        Your thought:
        {thought}
        
        Available tools:
        {tools_description}
        
        Respond in the following JSON format:
        {{
            "tool": "tool_name",
            "args": {{
                "arg1": "value1",
                "arg2": "value2"
            }}
        }}
        """
        
        # 生成行動
        action_json = self.llm.generate(prompt, self.system_prompt)
        
        # 解析JSON (實際實現中需要處理JSON解析錯誤)
        import json
        try:
            action_data = json.loads(action_json)
            action = Action(
                tool=action_data["tool"],
                args=action_data["args"],
                thought=thought
            )
        except (json.JSONDecodeError, KeyError):
            # 如果解析失敗，使用默認行動
            action = Action(
                tool="default_tool",
                args={"message": "Failed to parse action"},
                thought=thought
            )
        
        # 記錄行動
        self.memory.add({"type": "action", "content": str(action)})
        
        return action
    
    def observe(self, result: Any) -> str:
        """
        觀察結果，可以被子類重寫
        
        參數:
            result (Any): 行動結果
            
        返回:
            str: 觀察結果
        """
        # 記錄觀察
        observation = str(result)
        self.memory.add({"type": "observation", "content": observation})
        
        return observation
    
    def run(self, context: str) -> str:
        """
        執行代理的思考-行動-觀察循環
        
        參數:
            context (str): 上下文信息
            
        返回:
            str: 執行結果
        """
        # 記錄上下文
        self.memory.add({"type": "context", "content": context})
        
        # 思考
        thought = self.think(context)
        
        # 行動
        action = self.act(thought)
        
        # 執行行動
        result = self.execute_action(action)
        
        # 觀察
        observation = self.observe(result)
        
        return observation
    
    def register_tool(self, tool_name: str, tool_function: Callable) -> None:
        """
        註冊工具
        
        參數:
            tool_name (str): 工具名稱
            tool_function (Callable): 工具函數
        """
        self.tools[tool_name] = tool_function
    
    def execute_action(self, action: Action) -> Any:
        """
        執行動作，調用相應的工具
        
        參數:
            action (Action): 行動
            
        返回:
            Any: 執行結果
            
        異常:
            Exception: 如果工具不存在
        """
        if action.tool in self.tools:
            return self.tools[action.tool](**action.args)
        else:
            raise Exception(f"Tool {action.tool} not found")
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        設置系統提示
        
        參數:
            prompt (str): 系統提示
        """
        self.system_prompt = prompt

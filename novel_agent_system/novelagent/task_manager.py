"""
任務管理器模組 - 負責分解和分配任務
"""

from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseAgent


class TaskManager:
    """
    任務管理器，負責分解和分配任務
    
    屬性:
        tasks (List[Dict[str, Any]]): 任務列表
        llm_interface: LLM接口，用於任務分解
    """
    
    def __init__(self, llm_config: Dict[str, Any]):
        """
        初始化任務管理器
        
        參數:
            llm_config (Dict[str, Any]): LLM配置
        """
        from .llm_interface import LLMInterface
        self.tasks = []
        self.llm_interface = LLMInterface(llm_config)
    
    def add_task(self, task: Dict[str, Any]) -> None:
        """
        添加任務
        
        參數:
            task (Dict[str, Any]): 任務信息
        """
        self.tasks.append(task)
    
    def decompose_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分解任務為子任務
        
        參數:
            task (Dict[str, Any]): 任務信息
            
        返回:
            List[Dict[str, Any]]: 子任務列表
        """
        # 構建提示
        prompt = f"""
        Please decompose the following task into smaller, manageable subtasks:
        
        Task: {task.get('description', '')}
        
        For each subtask, provide:
        1. A clear description
        2. Any dependencies on other subtasks
        3. Estimated complexity (low, medium, high)
        
        Format your response as a JSON array of subtasks.
        """
        
        # 生成子任務
        response = self.llm_interface.generate(prompt)
        
        # 解析JSON (實際實現中需要處理JSON解析錯誤)
        import json
        try:
            subtasks = json.loads(response)
            
            # 添加父任務ID
            for subtask in subtasks:
                subtask["parent_id"] = task.get("id")
            
            return subtasks
        except json.JSONDecodeError:
            # 如果解析失敗，返回一個默認子任務
            return [{
                "description": "Failed to decompose task",
                "parent_id": task.get("id"),
                "dependencies": [],
                "complexity": "medium"
            }]
    
    def assign_task(self, task: Dict[str, Any], agent: BaseAgent) -> str:
        """
        分配任務給代理
        
        參數:
            task (Dict[str, Any]): 任務信息
            agent (BaseAgent): 代理
            
        返回:
            str: 執行結果
        """
        # 構建任務上下文
        context = f"""
        Task: {task.get('description', '')}
        
        Additional Information:
        {task.get('additional_info', '')}
        
        Dependencies:
        {', '.join(task.get('dependencies', []))}
        
        Please complete this task.
        """
        
        # 執行任務
        result = agent.run(context)
        
        # 更新任務狀態
        task["status"] = "completed"
        task["result"] = result
        
        return result
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """
        獲取待處理的任務
        
        返回:
            List[Dict[str, Any]]: 待處理的任務列表
        """
        return [task for task in self.tasks if task.get("status") != "completed"]
    
    def get_completed_tasks(self) -> List[Dict[str, Any]]:
        """
        獲取已完成的任務
        
        返回:
            List[Dict[str, Any]]: 已完成的任務列表
        """
        return [task for task in self.tasks if task.get("status") == "completed"]
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        根據ID獲取任務
        
        參數:
            task_id (str): 任務ID
            
        返回:
            Optional[Dict[str, Any]]: 任務信息
        """
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None
    
    def monitor_progress(self) -> Dict[str, Any]:
        """
        監控任務進度
        
        返回:
            Dict[str, Any]: 進度信息
        """
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = total - completed
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "progress_percentage": (completed / total * 100) if total > 0 else 0
        }

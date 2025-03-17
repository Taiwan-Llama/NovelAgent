"""
代理協作協調器模組 - 管理多個代理之間的協作
"""

from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseAgent


class AgentCoordinator:
    """
    代理協作協調器，負責管理多個代理之間的協作
    
    屬性:
        agents (Dict[str, BaseAgent]): 代理字典
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, llm_config: Dict[str, Any]):
        """
        初始化代理協作協調器
        
        參數:
            llm_config (Dict[str, Any]): LLM配置
        """
        from .llm_interface import LLMInterface
        self.agents = {}
        self.llm_config = llm_config
        self.llm_interface = LLMInterface(llm_config)
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        註冊代理
        
        參數:
            agent (BaseAgent): 代理
        """
        self.agents[agent.name] = agent
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        獲取代理
        
        參數:
            agent_name (str): 代理名稱
            
        返回:
            Optional[BaseAgent]: 代理
        """
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """
        列出所有代理
        
        返回:
            List[str]: 代理名稱列表
        """
        return list(self.agents.keys())
    
    def coordinate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        協調多個代理完成任務
        
        參數:
            task (Dict[str, Any]): 任務信息
            
        返回:
            Dict[str, Any]: 執行結果
        """
        # 分析任務，決定哪個代理最適合處理
        agent_selection_prompt = f"""
        Based on the following task, which agent would be best suited to handle it?
        
        Task: {task.get('description', '')}
        
        Available agents:
        {', '.join(self.list_agents())}
        
        Respond with just the name of the most suitable agent.
        """
        
        selected_agent_name = self.llm_interface.generate(agent_selection_prompt).strip()
        
        # 檢查選擇的代理是否存在
        if selected_agent_name not in self.agents:
            # 如果不存在，選擇第一個代理
            if self.agents:
                selected_agent_name = next(iter(self.agents))
            else:
                return {"error": "No agents available"}
        
        # 獲取選擇的代理
        selected_agent = self.agents[selected_agent_name]
        
        # 執行任務
        result = selected_agent.run(task.get('description', ''))
        
        return {
            "task": task,
            "agent": selected_agent_name,
            "result": result
        }
    
    def message_passing(self, from_agent: str, to_agent: str, message: str) -> str:
        """
        代理間消息傳遞
        
        參數:
            from_agent (str): 發送代理名稱
            to_agent (str): 接收代理名稱
            message (str): 消息內容
            
        返回:
            str: 接收代理的回應
            
        異常:
            Exception: 如果代理不存在
        """
        if to_agent not in self.agents:
            raise Exception(f"Agent {to_agent} not found")
        
        # 構建消息上下文
        context = f"""
        Message from {from_agent}:
        
        {message}
        
        Please respond to this message.
        """
        
        # 執行接收代理
        return self.agents[to_agent].run(context)
    
    def broadcast(self, from_agent: str, message: str) -> Dict[str, str]:
        """
        廣播消息給所有代理
        
        參數:
            from_agent (str): 發送代理名稱
            message (str): 消息內容
            
        返回:
            Dict[str, str]: 各代理的回應
        """
        responses = {}
        
        for agent_name, agent in self.agents.items():
            if agent_name != from_agent:
                # 構建消息上下文
                context = f"""
                Broadcast message from {from_agent}:
                
                {message}
                
                Please respond to this broadcast message.
                """
                
                # 執行代理
                responses[agent_name] = agent.run(context)
        
        return responses
    
    def collaborative_task(self, task: Dict[str, Any], agent_names: List[str]) -> Dict[str, Any]:
        """
        協作任務，多個代理共同完成
        
        參數:
            task (Dict[str, Any]): 任務信息
            agent_names (List[str]): 參與代理名稱列表
            
        返回:
            Dict[str, Any]: 執行結果
        """
        # 檢查所有代理是否存在
        for agent_name in agent_names:
            if agent_name not in self.agents:
                return {"error": f"Agent {agent_name} not found"}
        
        # 分解任務
        task_decomposition_prompt = f"""
        Decompose the following task into subtasks for multiple agents to work on collaboratively:
        
        Task: {task.get('description', '')}
        
        Agents: {', '.join(agent_names)}
        
        For each subtask, specify which agent should handle it.
        Format your response as a JSON array of subtasks.
        """
        
        decomposition_result = self.llm_interface.generate(task_decomposition_prompt)
        
        # 解析JSON (實際實現中需要處理JSON解析錯誤)
        import json
        try:
            subtasks = json.loads(decomposition_result)
        except json.JSONDecodeError:
            return {"error": "Failed to decompose task"}
        
        # 執行子任務
        results = []
        for subtask in subtasks:
            agent_name = subtask.get("agent")
            if agent_name in self.agents:
                subtask_description = subtask.get("description", "")
                result = self.agents[agent_name].run(subtask_description)
                results.append({
                    "subtask": subtask,
                    "agent": agent_name,
                    "result": result
                })
        
        # 整合結果
        integration_prompt = f"""
        Integrate the following results from multiple agents into a cohesive response:
        
        Task: {task.get('description', '')}
        
        Results:
        {json.dumps(results, indent=2)}
        
        Provide a comprehensive and integrated response.
        """
        
        integrated_result = self.llm_interface.generate(integration_prompt)
        
        return {
            "task": task,
            "agents": agent_names,
            "subtask_results": results,
            "integrated_result": integrated_result
        }

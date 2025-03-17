#!/usr/bin/env python3
"""
多代理協作機制測試腳本
"""

import sys
import os
import json
from pathlib import Path

# 添加項目根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from novelagent.base_agent import BaseAgent
from novelagent.agent_coordinator import AgentCoordinator
from novelagent.task_manager import TaskManager
from novelagent.agents.novel_planner_agent import NovelPlannerAgent
from novelagent.agents.character_designer_agent import CharacterDesignerAgent


def test_agent_coordinator():
    """測試代理協調器"""
    print("測試代理協調器...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建代理
    planner = NovelPlannerAgent("Planner", llm_config)
    character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
    
    # 創建代理協調器
    coordinator = AgentCoordinator()
    
    # 註冊代理
    coordinator.register_agent(planner)
    coordinator.register_agent(character_designer)
    
    # 測試代理註冊
    agents = coordinator.get_all_agents()
    assert len(agents) == 2, f"註冊代理數量錯誤: {len(agents)}"
    assert "Planner" in [agent.name for agent in agents], "找不到Planner代理"
    assert "CharacterDesigner" in [agent.name for agent in agents], "找不到CharacterDesigner代理"
    
    # 測試獲取特定代理
    retrieved_planner = coordinator.get_agent("Planner")
    assert retrieved_planner.name == "Planner", f"獲取的代理名稱錯誤: {retrieved_planner.name}"
    
    print("代理協調器測試通過！")


def test_task_manager():
    """測試任務管理器"""
    print("\n測試任務管理器...")
    
    # 創建任務管理器
    task_manager = TaskManager()
    
    # 添加任務
    task_manager.add_task("task1", "創建小說大綱", {"priority": "high"})
    task_manager.add_task("task2", "設計角色", {"priority": "medium", "depends_on": "task1"})
    task_manager.add_task("task3", "撰寫第一章", {"priority": "low", "depends_on": "task2"})
    
    # 測試獲取任務
    all_tasks = task_manager.get_all_tasks()
    assert len(all_tasks) == 3, f"任務數量錯誤: {len(all_tasks)}"
    
    # 測試獲取下一個任務
    next_task = task_manager.get_next_task()
    assert next_task["id"] == "task1", f"下一個任務ID錯誤: {next_task['id']}"
    
    # 測試完成任務
    task_manager.complete_task("task1")
    next_task = task_manager.get_next_task()
    assert next_task["id"] == "task2", f"完成任務後下一個任務ID錯誤: {next_task['id']}"
    
    # 測試獲取特定任務
    task = task_manager.get_task("task3")
    assert task["description"] == "撰寫第一章", f"獲取的任務描述錯誤: {task['description']}"
    
    print("任務管理器測試通過！")


def test_agent_collaboration():
    """測試代理協作"""
    print("\n測試代理協作...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建代理
    planner = NovelPlannerAgent("Planner", llm_config)
    character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
    
    # 創建代理協調器
    coordinator = AgentCoordinator()
    coordinator.register_agent(planner)
    coordinator.register_agent(character_designer)
    
    # 創建任務管理器
    task_manager = TaskManager()
    task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner"})
    task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
    
    # 模擬協作流程
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    assert agent.name == "Planner", f"任務分配錯誤: {agent.name}"
    
    # 模擬完成任務
    task_manager.complete_task("create_outline")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    assert agent.name == "CharacterDesigner", f"任務分配錯誤: {agent.name}"
    
    print("代理協作測試通過！")


def main():
    """主函數"""
    print("開始測試多代理協作機制...\n")
    
    # 運行測試
    test_agent_coordinator()
    test_task_manager()
    test_agent_collaboration()
    
    print("\n所有多代理協作機制測試通過！")


if __name__ == "__main__":
    main()

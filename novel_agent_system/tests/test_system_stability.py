#!/usr/bin/env python3
"""
系統穩定性與可擴展性測試腳本
"""

import sys
import os
import json
import time
from pathlib import Path

# 添加項目根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from novelagent.base_agent import BaseAgent
from novelagent.agent_coordinator import AgentCoordinator
from novelagent.task_manager import TaskManager
from novelagent.agents.novel_planner_agent import NovelPlannerAgent
from novelagent.agents.character_designer_agent import CharacterDesignerAgent
from novelagent.agents.world_building_agent import WorldBuildingAgent
from novelagent.agents.chapter_writer_agent import ChapterWriterAgent
from novelagent.agents.editor_agent import EditorAgent
from novelagent.agents.continuity_checker_agent import ContinuityCheckerAgent


def test_system_stability():
    """測試系統穩定性"""
    print("測試系統穩定性...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建代理協調器
    coordinator = AgentCoordinator()
    
    # 創建並註冊多個代理
    for i in range(10):
        agent = BaseAgent(f"TestAgent{i}", "Tester", llm_config)
        coordinator.register_agent(agent)
    
    # 測試獲取所有代理
    agents = coordinator.get_all_agents()
    assert len(agents) == 10, f"註冊代理數量錯誤: {len(agents)}"
    
    # 測試獲取特定代理
    for i in range(10):
        agent = coordinator.get_agent(f"TestAgent{i}")
        assert agent is not None, f"無法獲取TestAgent{i}"
        assert agent.name == f"TestAgent{i}", f"代理名稱錯誤: {agent.name}"
    
    # 測試移除代理
    coordinator.remove_agent("TestAgent5")
    agents = coordinator.get_all_agents()
    assert len(agents) == 9, f"移除代理後數量錯誤: {len(agents)}"
    assert coordinator.get_agent("TestAgent5") is None, "已移除的代理仍然可以獲取"
    
    print("系統穩定性測試通過！")


def test_system_scalability():
    """測試系統可擴展性"""
    print("\n測試系統可擴展性...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建任務管理器
    task_manager = TaskManager()
    
    # 添加大量任務
    start_time = time.time()
    for i in range(1000):
        task_manager.add_task(f"task{i}", f"任務{i}描述", {"priority": i % 3})
    add_time = time.time() - start_time
    print(f"添加1000個任務耗時: {add_time:.4f}秒")
    
    # 測試獲取所有任務性能
    start_time = time.time()
    all_tasks = task_manager.get_all_tasks()
    get_time = time.time() - start_time
    print(f"獲取1000個任務耗時: {get_time:.4f}秒")
    assert len(all_tasks) == 1000, f"任務數量錯誤: {len(all_tasks)}"
    
    # 測試獲取下一個任務性能
    start_time = time.time()
    for i in range(100):
        task = task_manager.get_next_task()
        if task:
            task_manager.complete_task(task["id"])
    next_time = time.time() - start_time
    print(f"獲取並完成100個任務耗時: {next_time:.4f}秒")
    
    print("系統可擴展性測試通過！")


def test_model_adaptability():
    """測試模型適應性"""
    print("\n測試模型適應性...")
    
    # 測試不同模型配置
    model_configs = [
        {"model": "gpt-3.5-turbo", "api_key": "test_key", "temperature": 0.7},
        {"model": "gpt-4", "api_key": "test_key", "temperature": 0.5},
        {"model": "claude-3-opus", "api_key": "test_key", "temperature": 0.8},
        {"model": "llama-2-70b", "api_key": "test_key", "temperature": 0.6},
        {"model": "gemini-pro", "api_key": "test_key", "temperature": 0.7}
    ]
    
    # 為每個模型配置創建代理
    for config in model_configs:
        model_name = config["model"]
        print(f"測試 {model_name} 模型配置...")
        
        # 創建小說策劃代理
        planner = NovelPlannerAgent(f"{model_name}Planner", config)
        assert planner.llm_config["model"] == model_name, f"模型名稱錯誤: {planner.llm_config['model']}"
        
        # 創建角色設計代理
        character_designer = CharacterDesignerAgent(f"{model_name}CharacterDesigner", config)
        assert character_designer.llm_config["model"] == model_name, f"模型名稱錯誤: {character_designer.llm_config['model']}"
    
    print("模型適應性測試通過！")


def test_error_handling():
    """測試錯誤處理"""
    print("\n測試錯誤處理...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建代理協調器
    coordinator = AgentCoordinator()
    
    # 測試獲取不存在的代理
    non_existent_agent = coordinator.get_agent("NonExistentAgent")
    assert non_existent_agent is None, "獲取不存在的代理應該返回None"
    
    # 創建任務管理器
    task_manager = TaskManager()
    
    # 測試完成不存在的任務
    try:
        task_manager.complete_task("non_existent_task")
        print("完成不存在的任務時正確處理了錯誤")
    except Exception as e:
        assert False, f"完成不存在的任務時未正確處理錯誤: {e}"
    
    # 測試獲取不存在的任務
    non_existent_task = task_manager.get_task("non_existent_task")
    assert non_existent_task is None, "獲取不存在的任務應該返回None"
    
    print("錯誤處理測試通過！")


def main():
    """主函數"""
    print("開始測試系統穩定性與可擴展性...\n")
    
    # 運行測試
    test_system_stability()
    test_system_scalability()
    test_model_adaptability()
    test_error_handling()
    
    print("\n所有系統穩定性與可擴展性測試通過！")


if __name__ == "__main__":
    main()

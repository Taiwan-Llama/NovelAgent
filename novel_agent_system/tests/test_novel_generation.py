#!/usr/bin/env python3
"""
小說生成流程測試腳本
"""

import sys
import os
import json
from pathlib import Path

# 添加項目根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from novelagent.agents.novel_planner_agent import NovelPlannerAgent
from novelagent.agents.character_designer_agent import CharacterDesignerAgent
from novelagent.agents.world_building_agent import WorldBuildingAgent
from novelagent.agents.chapter_writer_agent import ChapterWriterAgent
from novelagent.agents.editor_agent import EditorAgent
from novelagent.agents.continuity_checker_agent import ContinuityCheckerAgent
from novelagent.agent_coordinator import AgentCoordinator
from novelagent.task_manager import TaskManager


def test_novel_generation_workflow():
    """測試小說生成工作流程"""
    print("測試小說生成工作流程...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建所有代理
    planner = NovelPlannerAgent("Planner", llm_config)
    character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
    world_builder = WorldBuildingAgent("WorldBuilder", llm_config)
    chapter_writer = ChapterWriterAgent("ChapterWriter", llm_config)
    editor = EditorAgent("Editor", llm_config)
    continuity_checker = ContinuityCheckerAgent("ContinuityChecker", llm_config)
    
    # 創建代理協調器
    coordinator = AgentCoordinator()
    
    # 註冊所有代理
    coordinator.register_agent(planner)
    coordinator.register_agent(character_designer)
    coordinator.register_agent(world_builder)
    coordinator.register_agent(chapter_writer)
    coordinator.register_agent(editor)
    coordinator.register_agent(continuity_checker)
    
    # 創建任務管理器
    task_manager = TaskManager()
    
    # 添加小說生成工作流程任務
    task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner"})
    task_manager.add_task("create_chapter_structure", "創建章節結構", {"assigned_to": "Planner", "depends_on": "create_outline"})
    task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
    task_manager.add_task("design_world", "設計世界觀", {"assigned_to": "WorldBuilder", "depends_on": "create_outline"})
    task_manager.add_task("create_continuity_notes", "創建連貫性筆記", {"assigned_to": "ContinuityChecker", "depends_on": "design_characters,design_world"})
    task_manager.add_task("write_chapter_1", "撰寫第一章", {"assigned_to": "ChapterWriter", "depends_on": "create_chapter_structure,design_characters,design_world"})
    task_manager.add_task("review_chapter_1", "審校第一章", {"assigned_to": "Editor", "depends_on": "write_chapter_1"})
    task_manager.add_task("check_continuity_chapter_1", "檢查第一章連貫性", {"assigned_to": "ContinuityChecker", "depends_on": "write_chapter_1"})
    
    # 測試工作流程執行順序
    expected_order = ["create_outline", "create_chapter_structure", "design_characters", "design_world", 
                      "create_continuity_notes", "write_chapter_1", "review_chapter_1", "check_continuity_chapter_1"]
    
    execution_order = []
    for _ in range(len(expected_order)):
        task = task_manager.get_next_task()
        if task:
            execution_order.append(task["id"])
            task_manager.complete_task(task["id"])
    
    # 驗證執行順序
    for i, task_id in enumerate(execution_order):
        assert task_id in expected_order, f"任務 {task_id} 不在預期執行順序中"
        if i > 0:
            # 檢查依賴關係
            current_idx = expected_order.index(task_id)
            prev_idx = expected_order.index(execution_order[i-1])
            assert current_idx > prev_idx or (current_idx == prev_idx + 1), f"任務 {task_id} 執行順序錯誤"
    
    print("小說生成工作流程測試通過！")


def test_novel_generation_integration():
    """測試小說生成集成"""
    print("\n測試小說生成集成...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建所有代理
    planner = NovelPlannerAgent("Planner", llm_config)
    character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
    world_builder = WorldBuildingAgent("WorldBuilder", llm_config)
    chapter_writer = ChapterWriterAgent("ChapterWriter", llm_config)
    editor = EditorAgent("Editor", llm_config)
    continuity_checker = ContinuityCheckerAgent("ContinuityChecker", llm_config)
    
    # 測試代理方法存在性
    assert hasattr(planner, "create_novel_outline"), "小說策劃代理缺少create_novel_outline方法"
    assert hasattr(character_designer, "create_character_profiles"), "角色設計代理缺少create_character_profiles方法"
    assert hasattr(world_builder, "create_world_setting"), "世界觀設計代理缺少create_world_setting方法"
    assert hasattr(chapter_writer, "write_chapter"), "章節撰寫代理缺少write_chapter方法"
    assert hasattr(editor, "review_chapter"), "編輯審校代理缺少review_chapter方法"
    assert hasattr(continuity_checker, "check_character_continuity"), "連貫性檢查代理缺少check_character_continuity方法"
    
    # 模擬小說生成流程（不實際調用LLM API）
    print("模擬小說生成流程...")
    print("1. 小說策劃代理創建小說大綱")
    print("2. 小說策劃代理創建章節結構")
    print("3. 角色設計代理創建角色檔案")
    print("4. 世界觀設計代理創建世界設定")
    print("5. 連貫性檢查代理創建連貫性筆記")
    print("6. 章節撰寫代理撰寫第一章")
    print("7. 編輯審校代理審校第一章")
    print("8. 連貫性檢查代理檢查第一章連貫性")
    
    print("小說生成集成測試通過！")


def main():
    """主函數"""
    print("開始測試小說生成流程...\n")
    
    # 運行測試
    test_novel_generation_workflow()
    test_novel_generation_integration()
    
    print("\n所有小說生成流程測試通過！")


if __name__ == "__main__":
    main()

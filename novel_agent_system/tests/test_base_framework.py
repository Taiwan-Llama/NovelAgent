#!/usr/bin/env python3
"""
基礎代理框架測試腳本
"""

import sys
import os
import json
from pathlib import Path

# 添加項目根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from novelagent.base_agent import BaseAgent
from novelagent.memory import Memory
from novelagent.llm_interface import LLMInterface


def test_base_agent():
    """測試基礎代理類"""
    print("測試基礎代理類...")
    
    # 創建測試配置
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    
    # 創建基礎代理
    agent = BaseAgent("TestAgent", "Tester", llm_config)
    
    # 測試代理屬性
    assert agent.name == "TestAgent", f"代理名稱錯誤: {agent.name}"
    assert agent.role == "Tester", f"代理角色錯誤: {agent.role}"
    assert agent.llm_config == llm_config, f"LLM配置錯誤: {agent.llm_config}"
    
    print("基礎代理類測試通過！")


def test_memory():
    """測試記憶系統"""
    print("\n測試記憶系統...")
    
    # 創建記憶系統
    memory = Memory()
    
    # 測試添加和檢索記憶
    memory.add("測試記憶1", {"type": "test", "importance": 5})
    memory.add("測試記憶2", {"type": "test", "importance": 3})
    memory.add("另一個記憶", {"type": "other", "importance": 4})
    
    # 測試檢索
    test_memories = memory.retrieve(query="測試", limit=2)
    assert len(test_memories) == 2, f"檢索記憶數量錯誤: {len(test_memories)}"
    
    # 測試按類型檢索
    type_memories = memory.retrieve_by_metadata("type", "test")
    assert len(type_memories) == 2, f"按類型檢索記憶數量錯誤: {len(type_memories)}"
    
    # 測試清除記憶
    memory.clear()
    all_memories = memory.retrieve(limit=10)
    assert len(all_memories) == 0, f"清除記憶後仍有記憶: {len(all_memories)}"
    
    print("記憶系統測試通過！")


def test_llm_interface():
    """測試LLM接口"""
    print("\n測試LLM接口...")
    
    # 創建LLM接口
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": "test_key",
        "temperature": 0.7
    }
    llm = LLMInterface(llm_config)
    
    # 測試LLM配置
    assert llm.config == llm_config, f"LLM配置錯誤: {llm.config}"
    
    # 由於無法實際調用API，僅測試接口存在
    assert hasattr(llm, "generate"), "LLM接口缺少generate方法"
    
    print("LLM接口測試通過！")


def main():
    """主函數"""
    print("開始測試基礎代理框架...\n")
    
    # 運行測試
    test_base_agent()
    test_memory()
    test_llm_interface()
    
    print("\n所有基礎代理框架測試通過！")


if __name__ == "__main__":
    main()

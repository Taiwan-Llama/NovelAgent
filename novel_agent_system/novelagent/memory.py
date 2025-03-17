"""
記憶系統模組 - 管理代理的上下文和長期記憶
"""

from typing import Dict, Any, List, Optional
import json
from .vector_db import VectorDB


class Memory:
    """
    記憶系統，負責管理代理的上下文和長期記憶
    
    屬性:
        short_term_memory (List[Dict[str, Any]]): 短期記憶，存儲最近的交互
        vector_db (Optional[VectorDB]): 向量數據庫，用於長期記憶
        max_short_term_items (int): 短期記憶的最大項目數
    """
    
    def __init__(self, vector_db_config: Optional[Dict[str, Any]] = None, max_short_term_items: int = 100):
        """
        初始化記憶系統
        
        參數:
            vector_db_config (Optional[Dict[str, Any]]): 向量數據庫配置
            max_short_term_items (int): 短期記憶的最大項目數
        """
        self.short_term_memory = []
        self.vector_db = VectorDB(vector_db_config) if vector_db_config else None
        self.max_short_term_items = max_short_term_items
    
    def add(self, item: Dict[str, Any], is_important: bool = False) -> None:
        """
        添加項目到記憶
        
        參數:
            item (Dict[str, Any]): 記憶項目
            is_important (bool): 是否為重要項目，如果為True則添加到向量數據庫
        """
        # 添加到短期記憶
        self.short_term_memory.append(item)
        
        # 如果短期記憶超過最大項目數，移除最舊的項目
        if len(self.short_term_memory) > self.max_short_term_items:
            self.short_term_memory.pop(0)
        
        # 如果是重要項目且向量數據庫存在，添加到向量數據庫
        if is_important and self.vector_db:
            self.vector_db.add(item)
    
    def get_recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        獲取最近的n個記憶項目
        
        參數:
            n (int): 項目數量
            
        返回:
            List[Dict[str, Any]]: 最近的記憶項目
        """
        return self.short_term_memory[-n:]
    
    def search(self, query: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相關記憶
        
        參數:
            query (str): 查詢字符串
            n (int): 返回結果數量
            
        返回:
            List[Dict[str, Any]]: 相關記憶項目
        """
        # 如果向量數據庫存在，從向量數據庫搜索
        if self.vector_db:
            return self.vector_db.search(query, n)
        
        # 否則，從短期記憶中簡單搜索
        results = []
        for item in self.short_term_memory:
            if query.lower() in json.dumps(item).lower():
                results.append(item)
                if len(results) >= n:
                    break
        
        return results
    
    def summarize(self, items: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        總結記憶項目
        
        參數:
            items (Optional[List[Dict[str, Any]]]): 要總結的項目，如果為None則總結所有短期記憶
            
        返回:
            str: 總結
        """
        items_to_summarize = items if items is not None else self.short_term_memory
        
        # 簡單的總結實現，實際應用中可能需要使用LLM生成更好的總結
        summary_parts = []
        for item in items_to_summarize:
            item_type = item.get("type", "unknown")
            content = item.get("content", "")
            summary_parts.append(f"{item_type}: {content[:100]}...")
        
        return "\n".join(summary_parts)
    
    def clear_short_term(self) -> None:
        """清空短期記憶"""
        self.short_term_memory = []
    
    def get_all_short_term(self) -> List[Dict[str, Any]]:
        """
        獲取所有短期記憶項目
        
        返回:
            List[Dict[str, Any]]: 所有短期記憶項目
        """
        return self.short_term_memory.copy()
    
    def get_by_type(self, item_type: str) -> List[Dict[str, Any]]:
        """
        獲取指定類型的記憶項目
        
        參數:
            item_type (str): 項目類型
            
        返回:
            List[Dict[str, Any]]: 指定類型的記憶項目
        """
        return [item for item in self.short_term_memory if item.get("type") == item_type]

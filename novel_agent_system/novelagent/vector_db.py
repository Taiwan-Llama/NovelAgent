"""
向量數據庫接口模組 - 提供向量數據庫的存儲和檢索功能
"""

from typing import Dict, Any, List, Optional, Union
import json
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import requests


class VectorDB:
    """
    向量數據庫接口，提供向量數據庫的存儲和檢索功能
    
    屬性:
        connection: PostgreSQL連接
        embedding_model: 嵌入模型名稱
        table_name: 表名
        dimension: 向量維度
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化向量數據庫接口
        
        參數:
            config (Optional[Dict[str, Any]]): 配置信息
        """
        if config is None:
            config = {}
        
        self.connection = None
        self.embedding_model = config.get("embedding_model", "ollama/embeddings")
        self.table_name = config.get("table_name", "novel_knowledge")
        self.dimension = config.get("dimension", 1536)
        
        # 如果提供了連接信息，則建立連接
        if "host" in config:
            self.connection = psycopg2.connect(
                host=config.get("host", "localhost"),
                database=config.get("database", "vectordb"),
                user=config.get("user", "postgres"),
                password=config.get("password", ""),
                port=config.get("port", 5432)
            )
            
            # 初始化表
            self._initialize_table()
    
    def _initialize_table(self) -> None:
        """初始化向量數據庫表"""
        if not self.connection:
            return
        
        with self.connection.cursor() as cursor:
            # 創建pgvector擴展
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # 創建表
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding VECTOR({self.dimension}) NOT NULL,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # 創建索引
            cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS {self.table_name}_embedding_idx 
            ON {self.table_name} USING ivfflat (embedding vector_cosine_ops);
            """)
            
            self.connection.commit()
    
    def get_embedding(self, text: str) -> List[float]:
        """
        獲取文本的嵌入向量
        
        參數:
            text (str): 文本
            
        返回:
            List[float]: 嵌入向量
        """
        # 使用Ollama的嵌入API
        if self.embedding_model.startswith("ollama/"):
            model_name = self.embedding_model.split("/")[1]
            try:
                response = requests.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": model_name, "prompt": text}
                )
                return response.json()["embedding"]
            except Exception as e:
                print(f"Error getting embedding from Ollama: {e}")
                # 返回零向量作為後備
                return [0.0] * self.dimension
        
        # 使用LiteLLM支持的其他嵌入模型
        try:
            import litellm
            response = litellm.embedding(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding from LiteLLM: {e}")
            # 返回零向量作為後備
            return [0.0] * self.dimension
    
    def add(self, item: Dict[str, Any]) -> bool:
        """
        添加項目到向量數據庫
        
        參數:
            item (Dict[str, Any]): 項目
            
        返回:
            bool: 是否成功
        """
        if not self.connection:
            return False
        
        content = item.get("content", "")
        if not content:
            return False
        
        # 獲取嵌入向量
        embedding = self.get_embedding(content)
        
        # 準備元數據
        metadata = {k: v for k, v in item.items() if k != "content"}
        
        # 插入數據
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {self.table_name} (content, embedding, metadata)
                VALUES (%s, %s, %s)
                """,
                (content, embedding, json.dumps(metadata))
            )
            self.connection.commit()
        
        return True
    
    def search(self, query: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相關項目
        
        參數:
            query (str): 查詢字符串
            n (int): 返回結果數量
            
        返回:
            List[Dict[str, Any]]: 相關項目
        """
        if not self.connection:
            return []
        
        # 獲取查詢的嵌入向量
        query_embedding = self.get_embedding(query)
        
        # 搜索相似項目
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT content, metadata, embedding <=> %s AS distance
                FROM {self.table_name}
                ORDER BY distance
                LIMIT %s
                """,
                (query_embedding, n)
            )
            
            results = []
            for content, metadata_json, distance in cursor.fetchall():
                metadata = json.loads(metadata_json) if metadata_json else {}
                item = {"content": content, **metadata, "distance": distance}
                results.append(item)
            
            return results
    
    def delete(self, item_id: int) -> bool:
        """
        刪除項目
        
        參數:
            item_id (int): 項目ID
            
        返回:
            bool: 是否成功
        """
        if not self.connection:
            return False
        
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE id = %s",
                (item_id,)
            )
            self.connection.commit()
        
        return True
    
    def clear(self) -> bool:
        """
        清空表
        
        返回:
            bool: 是否成功
        """
        if not self.connection:
            return False
        
        with self.connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {self.table_name}")
            self.connection.commit()
        
        return True
    
    def close(self) -> None:
        """關閉連接"""
        if self.connection:
            self.connection.close()
            self.connection = None

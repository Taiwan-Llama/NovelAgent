#!/usr/bin/env python3
"""
測試向量數據庫和嵌入系統
"""

import sys
import json
import psycopg2
import numpy as np
import requests
from psycopg2.extras import Json

# 數據庫連接配置
DB_CONFIG = {
    "host": "localhost",
    "database": "novelagent",
    "user": "postgres",
    "password": ""
}

def get_embedding(text, model="all-MiniLM-L6-v2"):
    """
    使用Ollama獲取文本的嵌入向量
    
    參數:
        text (str): 要嵌入的文本
        model (str): 嵌入模型名稱
        
    返回:
        list: 嵌入向量
    """
    try:
        # 嘗試使用Ollama API
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model, "prompt": text}
        )
        
        if response.status_code == 200:
            return response.json().get("embedding", [])
        
        # 如果Ollama不可用，生成隨機向量作為測試
        print(f"Ollama API不可用，使用隨機向量: {response.status_code}")
        return list(np.random.rand(1536))
    except Exception as e:
        print(f"獲取嵌入向量時出錯: {e}")
        # 生成隨機向量作為測試
        return list(np.random.rand(1536))

def add_to_vector_db(content, metadata=None):
    """
    添加內容到向量數據庫
    
    參數:
        content (str): 文本內容
        metadata (dict): 元數據
        
    返回:
        bool: 是否成功
    """
    try:
        # 獲取嵌入向量
        embedding = get_embedding(content)
        
        # 連接數據庫
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 插入數據
        cursor.execute(
            "INSERT INTO novel_knowledge (content, embedding, metadata) VALUES (%s, %s, %s) RETURNING id",
            (content, embedding, Json(metadata) if metadata else None)
        )
        
        # 獲取插入的ID
        inserted_id = cursor.fetchone()[0]
        
        # 提交事務
        conn.commit()
        
        # 關閉連接
        cursor.close()
        conn.close()
        
        print(f"成功添加內容到向量數據庫，ID: {inserted_id}")
        return True
    except Exception as e:
        print(f"添加內容到向量數據庫時出錯: {e}")
        return False

def search_vector_db(query, limit=5):
    """
    搜索向量數據庫
    
    參數:
        query (str): 查詢文本
        limit (int): 返回結果數量
        
    返回:
        list: 搜索結果
    """
    try:
        # 獲取查詢的嵌入向量
        query_embedding = get_embedding(query)
        
        # 連接數據庫
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 搜索相似向量
        cursor.execute(
            """
            SELECT id, content, metadata, embedding <=> %s AS distance
            FROM novel_knowledge
            ORDER BY distance
            LIMIT %s
            """,
            (query_embedding, limit)
        )
        
        # 獲取結果
        results = []
        for id, content, metadata, distance in cursor.fetchall():
            results.append({
                "id": id,
                "content": content,
                "metadata": metadata,
                "distance": distance
            })
        
        # 關閉連接
        cursor.close()
        conn.close()
        
        return results
    except Exception as e:
        print(f"搜索向量數據庫時出錯: {e}")
        return []

def main():
    """主函數"""
    print("測試向量數據庫和嵌入系統")
    
    # 測試數據
    test_data = [
        {
            "content": "哈利波特是一個年輕的巫師，他在霍格華茲魔法學校學習魔法。",
            "metadata": {"type": "character_info", "name": "哈利波特", "source": "哈利波特系列"}
        },
        {
            "content": "佛瑞多·巴金斯是一個霍比特人，他繼承了魔戒並開始了一段冒險。",
            "metadata": {"type": "character_info", "name": "佛瑞多", "source": "魔戒"}
        },
        {
            "content": "龍母丹妮莉絲·坦格利安擁有三條龍，她試圖奪回鐵王座。",
            "metadata": {"type": "character_info", "name": "丹妮莉絲", "source": "冰與火之歌"}
        }
    ]
    
    # 添加測試數據
    for item in test_data:
        add_to_vector_db(item["content"], item["metadata"])
    
    # 測試搜索
    print("\n搜索測試:")
    
    queries = [
        "霍格華茲的巫師",
        "霍比特人和魔戒",
        "龍和王座"
    ]
    
    for query in queries:
        print(f"\n查詢: {query}")
        results = search_vector_db(query)
        
        for i, result in enumerate(results):
            print(f"結果 {i+1}:")
            print(f"  內容: {result['content']}")
            print(f"  元數據: {result['metadata']}")
            print(f"  距離: {result['distance']}")

if __name__ == "__main__":
    main()

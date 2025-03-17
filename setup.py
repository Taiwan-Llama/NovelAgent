#!/usr/bin/env python3
"""
NovelAgent 安裝腳本 - 設置 NovelAgent 系統環境
"""

import os
import sys
import subprocess
import argparse


def run_command(command, description=None):
    """執行命令並顯示結果"""
    if description:
        print(f"\n{description}...")
    
    print(f"執行: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("成功!")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print("失敗!")
        print(f"錯誤: {result.stderr.strip()}")
        sys.exit(1)


def setup_database():
    """設置 PostgreSQL 數據庫"""
    print("\n設置 PostgreSQL 數據庫...")
    
    # 啟動 PostgreSQL 服務
    run_command("sudo service postgresql start", "啟動 PostgreSQL 服務")
    
    # 創建數據庫
    run_command("sudo -u postgres psql -c \"CREATE DATABASE novelagent;\"", "創建 novelagent 數據庫")
    
    # 安裝 pgvector 擴展
    run_command("sudo -u postgres psql -d novelagent -c \"CREATE EXTENSION IF NOT EXISTS vector;\"", "安裝 pgvector 擴展")
    
    # 創建表和索引
    run_command("""
    sudo -u postgres psql -d novelagent -c "CREATE TABLE IF NOT EXISTS novel_knowledge (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        embedding vector(1536) NOT NULL,
        metadata JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"
    """, "創建 novel_knowledge 表")
    
    run_command("""
    sudo -u postgres psql -d novelagent -c "CREATE INDEX IF NOT EXISTS novel_knowledge_embedding_idx ON novel_knowledge USING ivfflat (embedding vector_cosine_ops);"
    """, "創建向量索引")
    
    print("\nPostgreSQL 數據庫設置完成!")


def install_dependencies(args):
    """安裝依賴庫"""
    print("\n安裝依賴庫...")
    
    # 安裝基本依賴
    dependencies = [
        "litellm",
        "psycopg2-binary",
        "langchain",
        "openai",
        "pgvector",
        "numpy",
        "pandas",
        "transformers"
    ]
    
    # 如果指定了 --dev 參數，添加開發依賴
    if args.dev:
        dependencies.extend([
            "pytest",
            "black",
            "flake8",
            "sphinx",
            "sphinx-rtd-theme"
        ])
    
    # 安裝依賴
    dependencies_str = " ".join(dependencies)
    run_command(f"pip install {dependencies_str}", "安裝 Python 依賴庫")
    
    print("\n依賴庫安裝完成!")


def create_directories():
    """創建必要的目錄"""
    print("\n創建目錄結構...")
    
    directories = [
        "novels",
        "logs",
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"創建目錄: {directory}")
    
    print("\n目錄結構創建完成!")


def create_config_file():
    """創建配置文件"""
    print("\n創建配置文件...")
    
    config_content = """
{
    "database": {
        "host": "localhost",
        "port": 5432,
        "database": "novelagent",
        "user": "postgres",
        "password": ""
    },
    "llm": {
        "default_model": "gpt-3.5-turbo",
        "api_key": "your_api_key_here",
        "temperature": 0.7
    },
    "embedding": {
        "model": "ollama/nomic-embed-text",
        "api_key": ""
    },
    "novel": {
        "default_output_dir": "novels",
        "default_chapter_length": 6000
    },
    "logging": {
        "level": "INFO",
        "file": "logs/novelagent.log"
    }
}
"""
    
    with open("config/config.json", "w") as f:
        f.write(config_content)
    
    print("配置文件已創建: config/config.json")
    print("請編輯配置文件，填入您的 API 密鑰和其他設置。")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="NovelAgent 安裝腳本")
    parser.add_argument("--skip-db", action="store_true", help="跳過數據庫設置")
    parser.add_argument("--dev", action="store_true", help="安裝開發依賴")
    args = parser.parse_args()
    
    print("=" * 60)
    print("NovelAgent 安裝腳本")
    print("=" * 60)
    
    # 安裝依賴庫
    install_dependencies(args)
    
    # 設置數據庫
    if not args.skip_db:
        setup_database()
    else:
        print("\n跳過數據庫設置。")
    
    # 創建目錄
    create_directories()
    
    # 創建配置文件
    create_config_file()
    
    print("\n" + "=" * 60)
    print("NovelAgent 安裝完成!")
    print("=" * 60)
    print("\n使用說明:")
    print("1. 編輯 config/config.json 文件，填入您的 API 密鑰和其他設置")
    print("2. 運行示例: python examples/novel_generation_example.py")
    print("3. 查看文檔: docs/system_documentation.md 和 docs/user_guide.md")
    print("\n祝您使用愉快!")


if __name__ == "__main__":
    main()

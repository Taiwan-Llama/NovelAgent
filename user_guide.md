# NovelAgent 使用指南

## 簡介

NovelAgent 是一個強大的多智能體系統，專為生成長篇小說而設計。本指南將幫助您快速上手使用 NovelAgent 系統，生成連貫的長篇小說。

## 快速開始

### 安裝

1. 確保您已安裝所需的依賴：

```bash
pip install litellm psycopg2-binary langchain openai pgvector numpy pandas transformers
```

2. 確保 PostgreSQL 數據庫已安裝並運行：

```bash
sudo service postgresql start
```

3. 設置數據庫：

```bash
sudo -u postgres psql -c "CREATE DATABASE novelagent;"
sudo -u postgres psql -d novelagent -c "CREATE EXTENSION IF NOT EXISTS vector;"
sudo -u postgres psql -d novelagent -c "CREATE TABLE novel_knowledge (id SERIAL PRIMARY KEY, content TEXT NOT NULL, embedding vector(1536) NOT NULL, metadata JSONB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
sudo -u postgres psql -d novelagent -c "CREATE INDEX novel_knowledge_embedding_idx ON novel_knowledge USING ivfflat (embedding vector_cosine_ops);"
```

### 基本用法

以下是使用 NovelAgent 生成小說的基本步驟：

```python
from novelagent.agent_coordinator import AgentCoordinator
from novelagent.task_manager import TaskManager
from novelagent.agents.novel_planner_agent import NovelPlannerAgent
from novelagent.agents.character_designer_agent import CharacterDesignerAgent
from novelagent.agents.world_building_agent import WorldBuildingAgent
from novelagent.agents.chapter_writer_agent import ChapterWriterAgent
from novelagent.agents.editor_agent import EditorAgent
from novelagent.agents.continuity_checker_agent import ContinuityCheckerAgent

# 配置 LLM
llm_config = {
    "model": "gpt-4",
    "api_key": "your_api_key",
    "temperature": 0.7
}

# 創建代理
planner = NovelPlannerAgent("Planner", llm_config)
character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
world_builder = WorldBuildingAgent("WorldBuilder", llm_config)
chapter_writer = ChapterWriterAgent("ChapterWriter", llm_config)
editor = EditorAgent("Editor", llm_config)
continuity_checker = ContinuityCheckerAgent("ContinuityChecker", llm_config)

# 創建代理協調器
coordinator = AgentCoordinator()
coordinator.register_agent(planner)
coordinator.register_agent(character_designer)
coordinator.register_agent(world_builder)
coordinator.register_agent(chapter_writer)
coordinator.register_agent(editor)
coordinator.register_agent(continuity_checker)

# 創建任務管理器
task_manager = TaskManager()

# 設置小說參數
novel_title = "魔法世界的冒險"
genre = "奇幻"
target_length = 300  # 300章

# 添加小說生成任務
task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner"})
task_manager.add_task("create_chapter_structure", "創建章節結構", {"assigned_to": "Planner", "depends_on": "create_outline"})
task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
task_manager.add_task("design_world", "設計世界觀", {"assigned_to": "WorldBuilder", "depends_on": "create_outline"})

# 執行小說生成流程
# 創建小說大綱
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
novel_outline = agent.create_novel_outline(novel_title, genre, target_length)
task_manager.complete_task(current_task["id"])

# 繼續執行其他任務...
```

## 生成完整小說

要生成完整的小說，請按照以下步驟操作：

1. 設置小說參數：
   - 標題
   - 類型
   - 目標章節數
   - 主題（可選）

2. 創建小說大綱和結構：
   - 使用 NovelPlannerAgent 創建小說大綱
   - 使用 NovelPlannerAgent 創建章節結構

3. 設計角色和世界：
   - 使用 CharacterDesignerAgent 創建角色檔案
   - 使用 WorldBuildingAgent 創建世界設定

4. 生成章節內容：
   - 使用 ChapterWriterAgent 撰寫章節
   - 使用 EditorAgent 審校章節
   - 使用 ContinuityCheckerAgent 檢查連貫性

5. 保存小說：
   - 將每章內容保存到單獨的文件中
   - 將小說元數據保存到數據庫

## 自定義選項

### 使用不同的語言模型

NovelAgent 支持任何 LiteLLM 支持的語言模型。您可以通過修改 llm_config 來使用不同的模型：

```python
# 使用 GPT-4
llm_config_gpt4 = {
    "model": "gpt-4",
    "api_key": "your_api_key",
    "temperature": 0.7
}

# 使用 Claude
llm_config_claude = {
    "model": "claude-3-opus",
    "api_key": "your_api_key",
    "temperature": 0.7
}

# 使用 Llama 2
llm_config_llama = {
    "model": "llama-2-70b",
    "api_key": "your_api_key",
    "temperature": 0.7
}
```

### 調整生成參數

您可以調整以下參數來自定義小說生成：

- **temperature**：控制生成文本的隨機性，值越高，生成的文本越隨機
- **主要角色數量**：影響小說的複雜度和角色互動
- **世界設定詳細程度**：影響小說的沉浸感和背景豐富度
- **章節長度**：控制每章的字數

### 保存和加載進度

您可以隨時保存和加載小說生成進度：

```python
import json

# 保存進度
def save_progress(filename, novel_data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(novel_data, f, ensure_ascii=False, indent=2)

# 加載進度
def load_progress(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 使用示例
novel_data = {
    "title": novel_title,
    "genre": genre,
    "outline": novel_outline,
    "chapter_structure": chapter_structure,
    "characters": character_profiles,
    "world_setting": world_setting,
    "current_chapter": 10
}

save_progress("novel_progress.json", novel_data)

# 稍後加載進度
loaded_data = load_progress("novel_progress.json")
```

## 常見問題解答

### Q: 生成小說需要多長時間？

A: 生成時間取決於小說的長度、複雜度和使用的語言模型。一本 300 章的小說可能需要數小時到數天不等。

### Q: 如何確保小說的連貫性？

A: NovelAgent 使用專門的 ContinuityCheckerAgent 來檢查角色、情節、世界設定和時間線的連貫性，並使用向量數據庫存儲和檢索相關信息。

### Q: 可以中途修改小說的方向嗎？

A: 可以。您可以修改小說大綱或章節結構，然後繼續生成後續章節。系統會自動適應新的方向。

### Q: 如何處理 API 限制？

A: 您可以實現重試機制和速率限制，或者使用本地部署的模型來避免 API 限制。

## 進階功能

### 多模型協作

您可以為不同的代理分配不同的語言模型，以優化性能和成本：

```python
# 為不同代理使用不同模型
planner_config = {"model": "gpt-4", "api_key": "your_api_key", "temperature": 0.7}
writer_config = {"model": "claude-3-opus", "api_key": "your_api_key", "temperature": 0.8}
editor_config = {"model": "gpt-3.5-turbo", "api_key": "your_api_key", "temperature": 0.5}

planner = NovelPlannerAgent("Planner", planner_config)
chapter_writer = ChapterWriterAgent("ChapterWriter", writer_config)
editor = EditorAgent("Editor", editor_config)
```

### 批量生成

您可以實現批量生成功能，同時處理多個章節：

```python
import concurrent.futures

def generate_chapters_batch(start_chapter, end_chapter):
    chapters = {}
    for i in range(start_chapter, end_chapter + 1):
        chapter_outline = chapter_structure.split(f"第{i}章")[1].split(f"第{i+1}章")[0] if i < target_length else chapter_structure.split(f"第{i}章")[1]
        previous_chapter_summary = chapter_summaries[i-2] if i > 1 and i-2 < len(chapter_summaries) else None
        chapter_content = chapter_writer.write_chapter(chapter_outline, character_profiles, previous_chapter_summary)
        chapters[i] = chapter_content
    return chapters

# 使用線程池批量生成章節
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    batch_size = 5
    futures = {}
    for batch_start in range(1, target_length + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, target_length)
        future = executor.submit(generate_chapters_batch, batch_start, batch_end)
        futures[future] = (batch_start, batch_end)
    
    for future in concurrent.futures.as_completed(futures):
        batch_start, batch_end = futures[future]
        try:
            chapters = future.result()
            for chapter_num, content in chapters.items():
                save_chapter(novel_title, chapter_num, content)
                print(f"已生成第 {chapter_num} 章")
        except Exception as e:
            print(f"生成章節 {batch_start}-{batch_end} 時出錯: {e}")
```

## 結語

NovelAgent 是一個強大而靈活的系統，能夠生成連貫的長篇小說。通過本指南，您應該能夠開始使用 NovelAgent 創建您自己的小說。如需更詳細的信息，請參閱系統文檔。

祝您創作愉快！

# NovelAgent 系統文檔

## 1. 系統概述

NovelAgent 是一個基於 Python 的多智能體系統，專為生成長篇小說而設計。系統使用 LiteLLM 的 API 和自定義的代理框架，以高度模組化的方式建立多智能體工具，能夠克服大型語言模型在生成長篇內容時的上下文限制，產生完整且連貫的長篇小說。

### 主要特點

- **多智能體協作**：專業化的代理角色分工合作，各司其職
- **長上下文管理**：使用分層概括機制和思想原子處理長上下文
- **向量數據庫支持**：使用 PostgreSQL 和 pgvector 進行知識管理
- **高度模組化**：簡潔的核心框架，易於擴展和自定義
- **模型靈活性**：支持任何 LiteLLM 支持的語言模型
- **標準操作流程**：精心設計的 SOP 確保小說生成的質量和連貫性

## 2. 系統架構

NovelAgent 系統由以下主要組件構成：

### 2.1 核心框架

- **BaseAgent**：所有代理的基礎類，實現思考-行動-觀察循環
- **Memory**：管理代理的上下文和長期記憶
- **VectorDB**：提供與 PostgreSQL 向量數據庫的交互功能
- **LLMInterface**：提供與語言模型的交互功能
- **TaskManager**：負責分解和分配任務
- **AgentCoordinator**：管理多個代理之間的協作
- **ThoughtAtom**：實現思想原子和分層概括機制

### 2.2 專業化代理

- **NovelPlannerAgent**：負責小說的整體規劃和構思
- **CharacterDesignerAgent**：負責創建角色檔案和角色關係
- **WorldBuildingAgent**：負責創建小說世界的設定和背景
- **ChapterWriterAgent**：負責撰寫小說章節內容
- **EditorAgent**：負責審校和修改小說內容
- **ContinuityCheckerAgent**：負責檢查小說內容的連貫性和一致性

### 2.3 數據庫系統

- **PostgreSQL**：關係型數據庫，用於存儲小說內容和元數據
- **pgvector**：PostgreSQL 擴展，提供向量搜索功能
- **向量表**：存儲章節摘要、角色信息、情節線跟踪和世界設定細節

## 3. 安裝指南

### 3.1 系統要求

- Python 3.8+
- PostgreSQL 14+
- pgvector 擴展

### 3.2 安裝步驟

1. 克隆代碼庫：

```bash
git clone https://github.com/yourusername/novelagent.git
cd novelagent
```

2. 安裝依賴：

```bash
pip install -r requirements.txt
```

3. 安裝 PostgreSQL 和 pgvector：

```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib postgresql-server-dev-all
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

4. 設置數據庫：

```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE novelagent;"
sudo -u postgres psql -d novelagent -c "CREATE EXTENSION IF NOT EXISTS vector;"
sudo -u postgres psql -d novelagent -c "CREATE TABLE novel_knowledge (id SERIAL PRIMARY KEY, content TEXT NOT NULL, embedding vector(1536) NOT NULL, metadata JSONB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
sudo -u postgres psql -d novelagent -c "CREATE INDEX novel_knowledge_embedding_idx ON novel_knowledge USING ivfflat (embedding vector_cosine_ops);"
```

## 4. 使用指南

### 4.1 基本用法

以下是使用 NovelAgent 生成小說的基本步驟：

1. 初始化系統：

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
```

2. 設置小說生成任務：

```python
# 添加小說生成工作流程任務
task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner"})
task_manager.add_task("create_chapter_structure", "創建章節結構", {"assigned_to": "Planner", "depends_on": "create_outline"})
task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
task_manager.add_task("design_world", "設計世界觀", {"assigned_to": "WorldBuilder", "depends_on": "create_outline"})
task_manager.add_task("create_continuity_notes", "創建連貫性筆記", {"assigned_to": "ContinuityChecker", "depends_on": "design_characters,design_world"})
```

3. 執行小說生成流程：

```python
# 執行任務
novel_title = "魔法世界的冒險"
genre = "奇幻"
target_length = 300  # 300章

# 創建小說大綱
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
novel_outline = agent.create_novel_outline(novel_title, genre, target_length)
task_manager.complete_task(current_task["id"])

# 創建章節結構
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
chapter_structure = agent.create_chapter_structure(novel_outline, target_length)
task_manager.complete_task(current_task["id"])

# 設計角色
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
character_profiles = agent.create_character_profiles(novel_outline, 5, 10)  # 5個主角，10個配角
task_manager.complete_task(current_task["id"])

# 設計世界觀
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
world_setting = agent.create_world_setting(novel_outline, genre)
task_manager.complete_task(current_task["id"])

# 創建連貫性筆記
current_task = task_manager.get_next_task()
agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
continuity_notes = agent.generate_continuity_notes(novel_outline, character_profiles, world_setting)
task_manager.complete_task(current_task["id"])
```

4. 生成章節：

```python
# 為每個章節添加任務
for i in range(1, target_length + 1):
    task_manager.add_task(f"write_chapter_{i}", f"撰寫第{i}章", {"assigned_to": "ChapterWriter", "depends_on": "create_continuity_notes" if i == 1 else f"check_continuity_chapter_{i-1}"})
    task_manager.add_task(f"review_chapter_{i}", f"審校第{i}章", {"assigned_to": "Editor", "depends_on": f"write_chapter_{i}"})
    task_manager.add_task(f"check_continuity_chapter_{i}", f"檢查第{i}章連貫性", {"assigned_to": "ContinuityChecker", "depends_on": f"review_chapter_{i}"})

# 生成章節內容
chapter_summaries = []
for i in range(1, target_length + 1):
    # 撰寫章節
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    chapter_outline = chapter_structure.split(f"第{i}章")[1].split(f"第{i+1}章")[0] if i < target_length else chapter_structure.split(f"第{i}章")[1]
    previous_chapter_summary = chapter_summaries[-1] if chapter_summaries else None
    chapter_content = agent.write_chapter(chapter_outline, character_profiles, previous_chapter_summary)
    task_manager.complete_task(current_task["id"])
    
    # 審校章節
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    review_notes = agent.review_chapter(chapter_content, novel_style_guide)
    chapter_content = chapter_writer.revise_chapter(chapter_content, review_notes)
    task_manager.complete_task(current_task["id"])
    
    # 檢查連貫性
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    continuity_issues = agent.check_character_continuity(chapter_content, character_profiles, chapter_summaries)
    if continuity_issues:
        chapter_content = chapter_writer.revise_chapter(chapter_content, continuity_issues)
    task_manager.complete_task(current_task["id"])
    
    # 創建章節摘要並保存
    chapter_summary = chapter_writer.create_chapter_summary(chapter_content)
    chapter_summaries.append(chapter_summary)
    
    # 保存章節
    save_chapter(novel_title, i, chapter_content)
```

### 4.2 自定義代理

您可以通過繼承 BaseAgent 類來創建自定義代理：

```python
from novelagent.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Custom Agent", llm_config)
        self.system_prompt = f"You are {name}, a custom agent with specific capabilities."
    
    def my_custom_method(self, input_data):
        prompt = f"Process this data: {input_data}"
        return self.llm.generate(prompt, self.system_prompt)
```

## 5. API 文檔

### 5.1 BaseAgent

基礎代理類，所有專業化代理的父類。

**方法**：
- `__init__(name, role, llm_config)`: 初始化代理
- `think(input_data)`: 思考並生成回應
- `act(action_type, action_input)`: 執行動作
- `observe(observation)`: 觀察結果

### 5.2 Memory

記憶系統，管理代理的上下文和長期記憶。

**方法**：
- `add(content, metadata)`: 添加記憶
- `retrieve(query, limit)`: 檢索記憶
- `retrieve_by_metadata(key, value)`: 按元數據檢索記憶
- `clear()`: 清除所有記憶

### 5.3 VectorDB

向量數據庫接口，提供與 PostgreSQL 向量數據庫的交互功能。

**方法**：
- `connect()`: 連接數據庫
- `add_embedding(content, embedding, metadata)`: 添加嵌入向量
- `search_similar(query_embedding, limit)`: 搜索相似向量
- `delete_embedding(id)`: 刪除嵌入向量

### 5.4 LLMInterface

語言模型接口，提供與語言模型的交互功能。

**方法**：
- `generate(prompt, system_prompt)`: 生成文本
- `get_embedding(text)`: 獲取文本的嵌入向量

### 5.5 TaskManager

任務管理器，負責分解和分配任務。

**方法**：
- `add_task(id, description, metadata)`: 添加任務
- `get_task(id)`: 獲取特定任務
- `get_all_tasks()`: 獲取所有任務
- `get_next_task()`: 獲取下一個任務
- `complete_task(id)`: 完成任務

### 5.6 AgentCoordinator

代理協調器，管理多個代理之間的協作。

**方法**：
- `register_agent(agent)`: 註冊代理
- `get_agent(name)`: 獲取特定代理
- `get_all_agents()`: 獲取所有代理
- `remove_agent(name)`: 移除代理

### 5.7 專業化代理

#### 5.7.1 NovelPlannerAgent

小說策劃代理，負責小說的整體規劃和構思。

**方法**：
- `create_novel_outline(title, genre, target_length, theme)`: 創建小說大綱
- `create_chapter_structure(novel_outline, num_chapters)`: 創建章節結構
- `design_story_arcs(novel_outline, main_characters)`: 設計故事弧

#### 5.7.2 CharacterDesignerAgent

角色設計代理，負責創建角色檔案和角色關係。

**方法**：
- `create_character_profiles(novel_outline, num_main_characters, num_supporting_characters)`: 創建角色檔案
- `design_character_relationships(character_profiles)`: 設計角色關係
- `plan_character_arcs(character_profiles, novel_outline)`: 規劃角色發展弧

#### 5.7.3 WorldBuildingAgent

世界觀設計代理，負責創建小說世界的設定和背景。

**方法**：
- `create_world_setting(novel_outline, genre)`: 創建世界設定
- `design_locations(world_setting, num_locations)`: 設計地點
- `create_history_and_lore(world_setting)`: 創建歷史和傳說
- `design_cultures_and_societies(world_setting, num_cultures)`: 設計文化和社會

#### 5.7.4 ChapterWriterAgent

章節撰寫代理，負責撰寫小說章節內容。

**方法**：
- `write_chapter(chapter_outline, character_profiles, previous_chapter_summary)`: 撰寫章節
- `create_chapter_summary(chapter_content)`: 創建章節摘要
- `revise_chapter(chapter_content, revision_notes)`: 修改章節

#### 5.7.5 EditorAgent

編輯審校代理，負責審校和修改小說內容。

**方法**：
- `review_chapter(chapter_content, novel_style_guide)`: 審校章節
- `improve_prose(text, style_notes)`: 改進文筆
- `check_pacing(chapter_content, chapter_outline)`: 檢查節奏
- `create_style_guide(sample_chapters, genre)`: 創建風格指南

#### 5.7.6 ContinuityCheckerAgent

連貫性檢查代理，負責檢查小說內容的連貫性和一致性。

**方法**：
- `check_character_continuity(chapter_content, character_profiles, previous_chapters_summaries)`: 檢查角色連貫性
- `check_plot_continuity(chapter_content, novel_outline, previous_chapters_summaries)`: 檢查情節連貫性
- `check_world_building_continuity(chapter_content, world_setting, previous_chapters_summaries)`: 檢查世界觀連貫性
- `check_timeline_consistency(chapter_content, previous_chapters_summaries)`: 檢查時間線一致性
- `generate_continuity_notes(novel_outline, character_profiles, world_setting)`: 生成連貫性筆記

## 6. 擴展和自定義

### 6.1 添加新代理

您可以通過繼承 BaseAgent 類來添加新的專業化代理：

```python
from novelagent.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "My New Role", llm_config)
        self.system_prompt = f"You are {name}, a specialized agent for..."
    
    def my_specialized_method(self, input_data):
        prompt = self._build_specialized_prompt(input_data)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_specialized_prompt(self, input_data):
        return f"Process this data: {input_data}"
```

### 6.2 使用不同的語言模型

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

### 6.3 自定義工作流程

您可以通過修改任務管理器中的任務來自定義小說生成工作流程：

```python
# 自定義工作流程
task_manager = TaskManager()

# 添加自定義任務
task_manager.add_task("research_historical_period", "研究歷史時期", {"assigned_to": "WorldBuilder"})
task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner", "depends_on": "research_historical_period"})
task_manager.add_task("create_language_guide", "創建語言指南", {"assigned_to": "WorldBuilder", "depends_on": "create_outline"})
task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
```

## 7. 故障排除

### 7.1 常見問題

1. **數據庫連接錯誤**

   問題：無法連接到 PostgreSQL 數據庫
   
   解決方案：
   - 確保 PostgreSQL 服務正在運行：`sudo service postgresql status`
   - 檢查數據庫配置是否正確
   - 確保 pgvector 擴展已安裝：`sudo -u postgres psql -d novelagent -c "SELECT * FROM pg_extension;"`

2. **API 密鑰錯誤**

   問題：LLM API 調用失敗
   
   解決方案：
   - 檢查 API 密鑰是否正確
   - 確保有足夠的 API 額度
   - 檢查網絡連接

3. **記憶體不足**

   問題：處理大型小說時出現記憶體錯誤
   
   解決方案：
   - 減少批處理大小
   - 使用流式處理
   - 增加系統記憶體

### 7.2 日誌和調試

NovelAgent 使用 Python 的 logging 模組進行日誌記錄。您可以通過以下方式配置日誌：

```python
import logging

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("novelagent.log"),
        logging.StreamHandler()
    ]
)

# 獲取日誌記錄器
logger = logging.getLogger("novelagent")
```

## 8. 結論

NovelAgent 是一個強大的多智能體系統，專為生成長篇小說而設計。通過專業化的代理角色分工合作，結合分層概括機制和思想原子處理長上下文，系統能夠克服大型語言模型在生成長篇內容時的上下文限制，產生完整且連貫的長篇小說。

系統的高度模組化設計使其易於擴展和自定義，支持任何 LiteLLM 支持的語言模型，並提供了完整的 API 和工具集，幫助您生成高質量的長篇小說。

## 9. 附錄

### 9.1 依賴庫

- litellm
- psycopg2-binary
- langchain
- openai
- pgvector
- numpy
- pandas
- transformers

### 9.2 參考資料

- Self-Supervised Prompt Optimization
- Atom of Thoughts for Markov LLM Test-Time Scaling
- Executable Code Actions Elicit Better LLM Agents
- ReAct agent 框架
- SmolaGent 框架

### 9.3 版本歷史

- v0.1.0：初始版本，實現基本功能
- v0.2.0：添加向量數據庫支持
- v0.3.0：實現分層概括機制
- v0.4.0：添加思想原子機制
- v0.5.0：完善連貫性檢查功能
- v1.0.0：正式發布版本

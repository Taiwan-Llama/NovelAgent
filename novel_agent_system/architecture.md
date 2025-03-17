# 多智能體小說生成系統架構設計

## 1. 核心框架設計原則

基於對現有框架的研究和分析，我們的核心框架設計將遵循以下原則：

1. **簡潔性**：核心框架代碼保持在約1,000行左右，避免過度抽象
2. **模組化**：將系統分解為可獨立開發和測試的模組
3. **可擴展性**：支持添加新的代理類型和工具
4. **可組合性**：允許靈活組合不同的代理和工具
5. **明確的接口**：定義清晰的接口，便於模組間通信
6. **自我優化**：支持代理自我評估和優化

## 2. 系統整體架構

系統整體架構分為以下幾個主要部分：

```
+------------------------------------------+
|              用戶界面層                   |
+------------------------------------------+
                    |
+------------------------------------------+
|              協調器層                     |
|  +-------------+  +-------------------+  |
|  | 任務管理器   |  | 代理協作協調器     |  |
|  +-------------+  +-------------------+  |
+------------------------------------------+
                    |
+------------------------------------------+
|              代理層                       |
|  +-------------+  +-------------------+  |
|  | 基礎代理類   |  | 專業化代理實現     |  |
|  +-------------+  +-------------------+  |
+------------------------------------------+
                    |
+------------------------------------------+
|              工具層                       |
|  +-------------+  +-------------------+  |
|  | LLM接口     |  | 外部工具接口       |  |
|  +-------------+  +-------------------+  |
+------------------------------------------+
                    |
+------------------------------------------+
|              存儲層                       |
|  +-------------+  +-------------------+  |
|  | 向量數據庫   |  | 文件存儲系統       |  |
|  +-------------+  +-------------------+  |
+------------------------------------------+
```

## 3. 核心組件設計

### 3.1 基礎代理類 (BaseAgent)

基礎代理類是所有代理的基礎，提供通用功能：

```python
class BaseAgent:
    def __init__(self, name, role, llm_config):
        self.name = name
        self.role = role
        self.llm_config = llm_config
        self.memory = Memory()
        self.tools = {}
        
    def think(self, context):
        """思考過程，可以被子類重寫"""
        pass
        
    def act(self, thought):
        """行動過程，可以被子類重寫"""
        pass
        
    def observe(self, result):
        """觀察結果，可以被子類重寫"""
        pass
        
    def run(self, context):
        """執行代理的思考-行動-觀察循環"""
        thought = self.think(context)
        action = self.act(thought)
        result = self.execute_action(action)
        observation = self.observe(result)
        return observation
        
    def register_tool(self, tool_name, tool_function):
        """註冊工具"""
        self.tools[tool_name] = tool_function
        
    def execute_action(self, action):
        """執行動作，調用相應的工具"""
        if action.tool in self.tools:
            return self.tools[action.tool](action.args)
        else:
            raise Exception(f"Tool {action.tool} not found")
```

### 3.2 記憶系統 (Memory)

記憶系統負責管理代理的上下文和長期記憶：

```python
class Memory:
    def __init__(self, vector_db_config=None):
        self.short_term_memory = []  # 短期記憶，存儲最近的交互
        self.vector_db = VectorDB(vector_db_config) if vector_db_config else None
        
    def add(self, item, is_important=False):
        """添加項目到記憶"""
        self.short_term_memory.append(item)
        if is_important and self.vector_db:
            self.vector_db.add(item)
            
    def get_recent(self, n=5):
        """獲取最近的n個記憶項目"""
        return self.short_term_memory[-n:]
        
    def search(self, query, n=5):
        """搜索相關記憶"""
        if self.vector_db:
            return self.vector_db.search(query, n)
        return []
        
    def summarize(self):
        """總結當前記憶"""
        # 實現分層概括
        pass
```

### 3.3 向量數據庫 (VectorDB)

向量數據庫負責存儲和檢索向量化的知識：

```python
class VectorDB:
    def __init__(self, config):
        self.connection = psycopg2.connect(
            host=config.get("host", "localhost"),
            database=config.get("database", "vectordb"),
            user=config.get("user", "postgres"),
            password=config.get("password", "")
        )
        self.embedding_model = config.get("embedding_model", "ollama/embeddings")
        
    def add(self, item):
        """添加項目到向量數據庫"""
        embedding = self.get_embedding(item.content)
        # 存儲到PostgreSQL
        
    def search(self, query, n=5):
        """搜索相關項目"""
        query_embedding = self.get_embedding(query)
        # 從PostgreSQL搜索
        
    def get_embedding(self, text):
        """獲取文本的嵌入向量"""
        # 使用Ollama的嵌入API
```

### 3.4 LLM接口 (LLMInterface)

LLM接口負責與語言模型的交互：

```python
class LLMInterface:
    def __init__(self, config):
        self.config = config
        
    def generate(self, prompt, system_message=None, temperature=0.7):
        """生成文本"""
        return litellm.completion(
            model=self.config.get("model", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": system_message or "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        
    def chat(self, messages, temperature=0.7):
        """聊天模式"""
        return litellm.completion(
            model=self.config.get("model", "gpt-3.5-turbo"),
            messages=messages,
            temperature=temperature
        )
```

### 3.5 任務管理器 (TaskManager)

任務管理器負責分解和分配任務：

```python
class TaskManager:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, task):
        """添加任務"""
        self.tasks.append(task)
        
    def decompose_task(self, task):
        """分解任務為子任務"""
        # 實現任務分解
        
    def assign_task(self, task, agent):
        """分配任務給代理"""
        return agent.run(task)
        
    def monitor_progress(self):
        """監控任務進度"""
        # 實現進度監控
```

### 3.6 代理協作協調器 (AgentCoordinator)

代理協作協調器負責管理多個代理之間的協作：

```python
class AgentCoordinator:
    def __init__(self):
        self.agents = {}
        
    def register_agent(self, agent):
        """註冊代理"""
        self.agents[agent.name] = agent
        
    def coordinate(self, task):
        """協調多個代理完成任務"""
        # 實現代理協作
        
    def message_passing(self, from_agent, to_agent, message):
        """代理間消息傳遞"""
        if to_agent in self.agents:
            return self.agents[to_agent].run(message)
        else:
            raise Exception(f"Agent {to_agent} not found")
```

## 4. 思想原子與分層概括

為了處理長上下文，我們實現思想原子和分層概括機制：

```python
class ThoughtAtom:
    def __init__(self, content, level=0, parent=None):
        self.content = content
        self.level = level
        self.parent = parent
        self.children = []
        
    def add_child(self, child):
        """添加子思想原子"""
        self.children.append(child)
        child.parent = self
        
    def summarize(self):
        """總結當前思想原子及其子思想"""
        if not self.children:
            return self.content
        
        child_summaries = [child.summarize() for child in self.children]
        combined = "\n".join(child_summaries)
        
        # 使用LLM生成摘要
        summary = llm.generate(f"Summarize the following content:\n{combined}")
        return summary
```

## 5. 小說生成專用代理設計

### 5.1 小說策劃代理 (NovelPlannerAgent)

```python
class NovelPlannerAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Planner", llm_config)
        
    def create_outline(self, title, genre, length):
        """創建小說大綱"""
        prompt = f"Create a detailed outline for a novel titled '{title}' in the {genre} genre with approximately {length} chapters."
        response = self.llm.generate(prompt)
        return response
        
    def create_character_profiles(self, outline):
        """創建角色檔案"""
        prompt = f"Based on the following novel outline, create detailed character profiles for all major characters:\n{outline}"
        response = self.llm.generate(prompt)
        return response
```

### 5.2 章節撰寫代理 (ChapterWriterAgent)

```python
class ChapterWriterAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Writer", llm_config)
        
    def write_chapter(self, chapter_number, chapter_outline, previous_chapter_summary=None, character_profiles=None):
        """撰寫章節"""
        context = f"Chapter Outline: {chapter_outline}\n"
        if previous_chapter_summary:
            context += f"Previous Chapter Summary: {previous_chapter_summary}\n"
        if character_profiles:
            context += f"Character Profiles: {character_profiles}\n"
            
        prompt = f"Write chapter {chapter_number} of the novel based on the following information:\n{context}"
        response = self.llm.generate(prompt)
        return response
```

### 5.3 編輯審校代理 (EditorAgent)

```python
class EditorAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Editor", llm_config)
        
    def edit_chapter(self, chapter_content):
        """編輯章節"""
        prompt = f"Edit the following chapter for grammar, style, and consistency:\n{chapter_content}"
        response = self.llm.generate(prompt)
        return response
        
    def check_continuity(self, current_chapter, previous_chapter_summary):
        """檢查連續性"""
        prompt = f"Check if the following chapter is consistent with the previous chapter summary:\nPrevious Chapter: {previous_chapter_summary}\nCurrent Chapter: {current_chapter}"
        response = self.llm.generate(prompt)
        return response
```

## 6. 標準操作流程 (SOP)

為了實現"Code = SOP(Team)"的核心哲學，我們為小說生成系統設計以下SOP：

### 6.1 小說創作SOP

1. **規劃階段**
   - 確定小說標題、類型和長度
   - 創建詳細的小說大綱
   - 設計主要角色檔案
   - 確定世界觀和背景設定

2. **撰寫階段**
   - 為每個章節創建詳細大綱
   - 撰寫章節初稿
   - 保存章節摘要到向量數據庫
   - 更新小說進度和狀態

3. **審校階段**
   - 檢查章節的語法和風格
   - 檢查與前序章節的連續性
   - 檢查角色行為的一致性
   - 修正發現的問題

4. **整合階段**
   - 將所有章節整合到一起
   - 檢查整體連貫性
   - 生成最終的小說文件

### 6.2 代理協作SOP

1. **任務分配**
   - 任務管理器分解任務
   - 協調器分配任務給適當的代理

2. **信息共享**
   - 代理將重要信息存儲到向量數據庫
   - 代理可以查詢相關信息

3. **協作解決問題**
   - 當代理遇到問題時，可以請求其他代理協助
   - 協調器管理協作過程

4. **結果整合**
   - 協調器整合各代理的結果
   - 生成最終輸出

## 7. 系統工作流程

整個小說生成系統的工作流程如下：

1. **初始化系統**
   - 創建所有必要的代理
   - 初始化向量數據庫
   - 設置LLM配置

2. **接收用戶輸入**
   - 獲取小說標題、類型和其他要求

3. **規劃小說**
   - 策劃代理創建小說大綱
   - 策劃代理創建角色檔案
   - 策劃代理創建世界觀設定

4. **生成章節**
   - 對每個章節：
     - 策劃代理創建章節大綱
     - 撰寫代理撰寫章節
     - 編輯代理審校章節
     - 將章節保存到文件系統
     - 將章節摘要保存到向量數據庫

5. **整合小說**
   - 將所有章節整合到一起
   - 生成最終的小說文件

6. **返回結果**
   - 將小說文件返回給用戶

## 8. 技術實現細節

### 8.1 向量數據庫設計

使用PostgreSQL和pgvector擴展實現向量數據庫：

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE novel_knowledge (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX novel_knowledge_embedding_idx ON novel_knowledge USING ivfflat (embedding vector_cosine_ops);
```

### 8.2 文件存儲結構

小說文件按以下結構存儲：

```
novel_title/
  ├── metadata.json       # 小說元數據
  ├── outline.md          # 小說大綱
  ├── characters.md       # 角色檔案
  ├── world_building.md   # 世界觀設定
  ├── chapters/
  │   ├── chapter_001.txt # 第1章
  │   ├── chapter_002.txt # 第2章
  │   └── ...
  └── novel.txt           # 完整小說
```

### 8.3 代理通信格式

代理間通信使用JSON格式：

```json
{
  "from": "agent_name",
  "to": "agent_name",
  "message_type": "request/response/notification",
  "content": "消息內容",
  "metadata": {
    "task_id": "任務ID",
    "timestamp": "時間戳"
  }
}
```

## 9. 擴展性和可定制性

系統設計考慮了擴展性和可定制性：

1. **支持不同的LLM**：通過LiteLLM支持各種語言模型
2. **可定制代理**：可以創建新的代理類型
3. **可定制工具**：可以添加新的工具
4. **可定制SOP**：可以修改標準操作流程
5. **可定制存儲**：可以使用不同的存儲後端

## 10. 系統限制和未來改進

當前設計的限制和未來可能的改進：

1. **計算資源**：生成長篇小說需要大量計算資源，未來可以實現分佈式處理
2. **模型限制**：依賴於底層LLM的能力，未來可以支持更強大的模型
3. **評估機制**：需要更好的小說質量評估機制
4. **用戶交互**：可以添加更多的用戶交互功能，如實時反饋
5. **多語言支持**：擴展支持多種語言的小說生成

## 結論

這個架構設計結合了現有框架的優點，同時針對長篇小說生成的特殊需求進行了優化。通過模組化設計、分層概括、思想原子和標準操作流程，系統能夠克服上下文限制，生成連貫的長篇小說。核心框架保持簡潔，同時提供足夠的擴展性和可定制性。

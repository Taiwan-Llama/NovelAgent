# 小說生成系統設計

## 1. 系統概述

小說生成系統是基於我們的多智能體框架構建的專門應用，旨在生成連貫的長篇小說。系統採用AI團隊協作的形式，每個代理負責小說創作過程中的特定角色，共同完成從構思到最終成稿的整個流程。

## 2. 專業化代理角色設計

### 2.1 小說策劃代理 (NovelPlannerAgent)

**角色職責**：
- 負責小說的整體規劃和構思
- 創建小說大綱和章節結構
- 設計小說的主要情節線和故事弧
- 確定小說的主題和風格

**關鍵能力**：
- 故事結構設計
- 情節發展規劃
- 主題和風格定義
- 長篇作品的整體架構設計

```python
class NovelPlannerAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Novel Planner", llm_config)
        self.system_prompt = f"You are {name}, a professional novel planner. Your job is to create detailed novel outlines, plan story arcs, and design the overall structure of long-form fiction."
    
    def create_novel_outline(self, title, genre, target_length, theme=None):
        """創建小說大綱"""
        prompt = self._build_outline_prompt(title, genre, target_length, theme)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_chapter_structure(self, novel_outline, num_chapters):
        """創建章節結構"""
        prompt = self._build_chapter_structure_prompt(novel_outline, num_chapters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_story_arcs(self, novel_outline, main_characters):
        """設計故事弧"""
        prompt = self._build_story_arcs_prompt(novel_outline, main_characters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_outline_prompt(self, title, genre, target_length, theme):
        """構建大綱提示"""
        prompt = f"""
        Create a detailed outline for a novel with the following specifications:
        
        Title: {title}
        Genre: {genre}
        Target Length: {target_length} chapters
        """
        
        if theme:
            prompt += f"Theme: {theme}\n"
        
        prompt += """
        Your outline should include:
        1. A compelling premise
        2. The main conflict
        3. The setting and world-building elements
        4. The narrative structure
        5. Key plot points and turning points
        
        Be detailed and specific, providing a solid foundation for a novel of this length.
        """
        
        return prompt
```

### 2.2 角色設計代理 (CharacterDesignerAgent)

**角色職責**：
- 創建主要和次要角色的詳細檔案
- 設計角色關係網絡
- 確保角色發展與故事弧一致
- 維護角色行為和動機的一致性

**關鍵能力**：
- 角色心理分析
- 角色關係設計
- 角色發展規劃
- 角色一致性維護

```python
class CharacterDesignerAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Character Designer", llm_config)
        self.system_prompt = f"You are {name}, a professional character designer for novels. Your job is to create detailed character profiles, design character relationships, and ensure consistent character development throughout the story."
    
    def create_character_profiles(self, novel_outline, num_main_characters, num_supporting_characters):
        """創建角色檔案"""
        prompt = self._build_character_profiles_prompt(novel_outline, num_main_characters, num_supporting_characters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_character_relationships(self, character_profiles):
        """設計角色關係"""
        prompt = self._build_character_relationships_prompt(character_profiles)
        return self.llm.generate(prompt, self.system_prompt)
    
    def plan_character_arcs(self, character_profiles, novel_outline):
        """規劃角色發展弧"""
        prompt = self._build_character_arcs_prompt(character_profiles, novel_outline)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_character_profiles_prompt(self, novel_outline, num_main_characters, num_supporting_characters):
        """構建角色檔案提示"""
        prompt = f"""
        Based on the following novel outline, create detailed profiles for {num_main_characters} main characters and {num_supporting_characters} supporting characters:
        
        Novel Outline:
        {novel_outline}
        
        For each character, include:
        1. Name, age, and physical description
        2. Background and personal history
        3. Personality traits and quirks
        4. Goals, motivations, and conflicts
        5. Role in the story
        6. Key relationships with other characters
        
        Make these characters complex, believable, and suited to the story outlined above.
        """
        
        return prompt
```

### 2.3 世界觀設計代理 (WorldBuildingAgent)

**角色職責**：
- 創建小說的世界設定和背景
- 設計地理、歷史、文化和社會結構
- 確保世界觀的一致性和合理性
- 為故事提供豐富的背景環境

**關鍵能力**：
- 世界設定創建
- 文化和社會系統設計
- 歷史背景構建
- 地理環境設計

```python
class WorldBuildingAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "World Builder", llm_config)
        self.system_prompt = f"You are {name}, a professional world builder for novels. Your job is to create detailed and consistent world settings, including geography, history, culture, and social structures."
    
    def create_world_setting(self, novel_outline, genre):
        """創建世界設定"""
        prompt = self._build_world_setting_prompt(novel_outline, genre)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_cultural_systems(self, world_setting):
        """設計文化系統"""
        prompt = self._build_cultural_systems_prompt(world_setting)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_historical_background(self, world_setting, novel_outline):
        """創建歷史背景"""
        prompt = self._build_historical_background_prompt(world_setting, novel_outline)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_world_setting_prompt(self, novel_outline, genre):
        """構建世界設定提示"""
        prompt = f"""
        Based on the following novel outline and genre, create a detailed world setting:
        
        Novel Outline:
        {novel_outline}
        
        Genre:
        {genre}
        
        Your world setting should include:
        1. Geographic features and locations
        2. Political and social structures
        3. Economic systems
        4. Technological level
        5. Magical or supernatural elements (if applicable)
        6. Key locations relevant to the story
        
        Create a rich, immersive, and consistent world that serves as a compelling backdrop for the story.
        """
        
        return prompt
```

### 2.4 章節撰寫代理 (ChapterWriterAgent)

**角色職責**：
- 根據大綱和角色檔案撰寫章節內容
- 確保章節與整體故事結構一致
- 維護敘事風格和語調的一致性
- 實現章節間的平滑過渡

**關鍵能力**：
- 敘事技巧
- 對話創作
- 場景描寫
- 情感表達

```python
class ChapterWriterAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Chapter Writer", llm_config)
        self.system_prompt = f"You are {name}, a professional novel writer. Your job is to write engaging and cohesive chapters based on outlines and character profiles, maintaining consistent narrative style and tone."
    
    def write_chapter(self, chapter_number, chapter_outline, character_profiles, previous_chapter_summary=None, world_setting=None):
        """撰寫章節"""
        prompt = self._build_chapter_prompt(chapter_number, chapter_outline, character_profiles, previous_chapter_summary, world_setting)
        return self.llm.generate(prompt, self.system_prompt, temperature=0.8)
    
    def _build_chapter_prompt(self, chapter_number, chapter_outline, character_profiles, previous_chapter_summary, world_setting):
        """構建章節提示"""
        prompt = f"""
        Write Chapter {chapter_number} of a novel based on the following outline:
        
        Chapter Outline:
        {chapter_outline}
        
        Character Profiles:
        {character_profiles}
        """
        
        if previous_chapter_summary:
            prompt += f"""
            Previous Chapter Summary:
            {previous_chapter_summary}
            """
        
        if world_setting:
            prompt += f"""
            World Setting:
            {world_setting}
            """
        
        prompt += """
        Guidelines:
        1. Write a complete chapter of approximately 6,000 words
        2. Include engaging dialogue, vivid descriptions, and character development
        3. Maintain consistent characterization and narrative voice
        4. Ensure the chapter advances the plot while fitting into the overall story
        5. End the chapter in a way that encourages continued reading
        
        Write the full chapter text now.
        """
        
        return prompt
```

### 2.5 編輯審校代理 (EditorAgent)

**角色職責**：
- 審校章節內容，修正語法和風格問題
- 確保敘事連貫性和一致性
- 提供改進建議和修改意見
- 維護整體作品質量

**關鍵能力**：
- 文本編輯
- 風格一致性檢查
- 語法和拼寫檢查
- 敘事流暢性評估

```python
class EditorAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Editor", llm_config)
        self.system_prompt = f"You are {name}, a professional novel editor. Your job is to review and improve chapter content, ensuring narrative coherence, consistent style, and high overall quality."
    
    def edit_chapter(self, chapter_content, novel_style_guide=None):
        """編輯章節"""
        prompt = self._build_edit_prompt(chapter_content, novel_style_guide)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_continuity(self, current_chapter, previous_chapter_summary, character_profiles):
        """檢查連續性"""
        prompt = self._build_continuity_check_prompt(current_chapter, previous_chapter_summary, character_profiles)
        return self.llm.generate(prompt, self.system_prompt)
    
    def provide_feedback(self, chapter_content):
        """提供反饋"""
        prompt = self._build_feedback_prompt(chapter_content)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_edit_prompt(self, chapter_content, novel_style_guide):
        """構建編輯提示"""
        prompt = f"""
        Edit the following chapter for grammar, style, clarity, and overall quality:
        
        Chapter Content:
        {chapter_content}
        """
        
        if novel_style_guide:
            prompt += f"""
            Style Guide:
            {novel_style_guide}
            """
        
        prompt += """
        Your edits should:
        1. Fix any grammar, spelling, or punctuation errors
        2. Improve awkward or unclear phrasing
        3. Enhance dialogue and descriptions where needed
        4. Ensure consistent tone and style
        5. Maintain the author's voice while improving the overall quality
        
        Provide the fully edited chapter text.
        """
        
        return prompt
```

### 2.6 連貫性檢查代理 (ContinuityCheckerAgent)

**角色職責**：
- 檢查小說內容的連貫性和一致性
- 識別和修正情節漏洞和矛盾
- 確保角色行為和設定的一致性
- 維護時間線和事件順序的合理性

**關鍵能力**：
- 情節一致性檢查
- 角色一致性檢查
- 時間線驗證
- 世界設定一致性檢查

```python
class ContinuityCheckerAgent(BaseAgent):
    def __init__(self, name, llm_config):
        super().__init__(name, "Continuity Checker", llm_config)
        self.system_prompt = f"You are {name}, a professional continuity checker for novels. Your job is to identify and fix plot holes, contradictions, and inconsistencies in character behavior, settings, and timelines."
    
    def check_plot_consistency(self, chapter_content, novel_outline, previous_chapters_summary):
        """檢查情節一致性"""
        prompt = self._build_plot_consistency_prompt(chapter_content, novel_outline, previous_chapters_summary)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_character_consistency(self, chapter_content, character_profiles, character_arcs):
        """檢查角色一致性"""
        prompt = self._build_character_consistency_prompt(chapter_content, character_profiles, character_arcs)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_timeline_consistency(self, chapter_content, timeline):
        """檢查時間線一致性"""
        prompt = self._build_timeline_consistency_prompt(chapter_content, timeline)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_plot_consistency_prompt(self, chapter_content, novel_outline, previous_chapters_summary):
        """構建情節一致性檢查提示"""
        prompt = f"""
        Check the following chapter for plot consistency with the novel outline and previous chapters:
        
        Chapter Content:
        {chapter_content}
        
        Novel Outline:
        {novel_outline}
        
        Previous Chapters Summary:
        {previous_chapters_summary}
        
        Identify any:
        1. Plot holes or logical inconsistencies
        2. Events that contradict the established outline
        3. Actions that don't follow from previous chapters
        4. Unexplained shifts in story direction
        
        For each issue found, explain the problem and suggest a specific fix.
        If no issues are found, confirm the plot consistency.
        """
        
        return prompt
```

## 3. 小說生成工作流程

小說生成系統的工作流程分為以下幾個階段：

### 3.1 規劃階段

1. **初始化系統**
   - 創建所有必要的代理
   - 初始化向量數據庫
   - 設置LLM配置

2. **接收用戶輸入**
   - 獲取小說標題、類型和其他要求
   - 確定目標章節數和每章字數

3. **小說規劃**
   - 策劃代理創建小說大綱
   - 角色設計代理創建角色檔案
   - 世界觀設計代理創建世界設定
   - 策劃代理創建章節結構

```python
def planning_phase(title, genre, target_chapters, chapter_length, theme=None):
    """小說規劃階段"""
    # 初始化代理
    planner = NovelPlannerAgent("NovelPlanner", llm_config)
    character_designer = CharacterDesignerAgent("CharacterDesigner", llm_config)
    world_builder = WorldBuildingAgent("WorldBuilder", llm_config)
    
    # 創建小說大綱
    novel_outline = planner.create_novel_outline(title, genre, target_chapters, theme)
    
    # 創建章節結構
    chapter_structure = planner.create_chapter_structure(novel_outline, target_chapters)
    
    # 創建角色檔案
    character_profiles = character_designer.create_character_profiles(novel_outline, 3, 5)
    
    # 設計角色關係
    character_relationships = character_designer.design_character_relationships(character_profiles)
    
    # 規劃角色發展弧
    character_arcs = character_designer.plan_character_arcs(character_profiles, novel_outline)
    
    # 創建世界設定
    world_setting = world_builder.create_world_setting(novel_outline, genre)
    
    # 返回規劃結果
    return {
        "novel_outline": novel_outline,
        "chapter_structure": chapter_structure,
        "character_profiles": character_profiles,
        "character_relationships": character_relationships,
        "character_arcs": character_arcs,
        "world_setting": world_setting
    }
```

### 3.2 生成階段

1. **章節生成**
   - 對每個章節：
     - 撰寫代理根據章節大綱撰寫章節
     - 編輯代理審校章節
     - 連貫性檢查代理檢查連貫性
     - 將章節保存到文件系統
     - 將章節摘要保存到向量數據庫

2. **進度監控**
   - 任務管理器監控生成進度
   - 更新生成狀態和統計信息

```python
def generation_phase(planning_results, target_chapters, output_dir):
    """小說生成階段"""
    # 初始化代理
    writer = ChapterWriterAgent("ChapterWriter", llm_config)
    editor = EditorAgent("Editor", llm_config)
    continuity_checker = ContinuityCheckerAgent("ContinuityChecker", llm_config)
    
    # 初始化向量數據庫
    vector_db = VectorDB(vector_db_config)
    
    # 創建輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "chapters"), exist_ok=True)
    
    # 保存規劃結果
    with open(os.path.join(output_dir, "novel_outline.md"), "w") as f:
        f.write(planning_results["novel_outline"])
    
    with open(os.path.join(output_dir, "character_profiles.md"), "w") as f:
        f.write(planning_results["character_profiles"])
    
    with open(os.path.join(output_dir, "world_setting.md"), "w") as f:
        f.write(planning_results["world_setting"])
    
    # 初始化進度
    progress = {"total": target_chapters, "completed": 0}
    
    # 初始化前一章摘要
    previous_chapter_summary = None
    
    # 生成章節
    for chapter_num in range(1, target_chapters + 1):
        print(f"Generating Chapter {chapter_num}...")
        
        # 獲取章節大綱
        chapter_outline = planning_results["chapter_structure"].split("Chapter " + str(chapter_num))[1].split("Chapter " + str(chapter_num + 1))[0]
        if chapter_num == target_chapters:
            chapter_outline = planning_results["chapter_structure"].split("Chapter " + str(chapter_num))[1]
        
        # 撰寫章節
        chapter_conten<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>
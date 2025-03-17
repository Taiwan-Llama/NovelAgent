"""
小說策劃代理模組 - 負責小說的整體規劃和構思
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class NovelPlannerAgent(BaseAgent):
    """
    小說策劃代理，負責小說的整體規劃和構思
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化小說策劃代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "Novel Planner", llm_config)
        self.system_prompt = f"You are {name}, a professional novel planner. Your job is to create detailed novel outlines, plan story arcs, and design the overall structure of long-form fiction."
    
    def create_novel_outline(self, title: str, genre: str, target_length: int, theme: Optional[str] = None) -> str:
        """
        創建小說大綱
        
        參數:
            title (str): 小說標題
            genre (str): 小說類型
            target_length (int): 目標章節數
            theme (Optional[str]): 小說主題
            
        返回:
            str: 小說大綱
        """
        prompt = self._build_outline_prompt(title, genre, target_length, theme)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_chapter_structure(self, novel_outline: str, num_chapters: int) -> str:
        """
        創建章節結構
        
        參數:
            novel_outline (str): 小說大綱
            num_chapters (int): 章節數量
            
        返回:
            str: 章節結構
        """
        prompt = self._build_chapter_structure_prompt(novel_outline, num_chapters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_story_arcs(self, novel_outline: str, main_characters: str) -> str:
        """
        設計故事弧
        
        參數:
            novel_outline (str): 小說大綱
            main_characters (str): 主要角色
            
        返回:
            str: 故事弧
        """
        prompt = self._build_story_arcs_prompt(novel_outline, main_characters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_outline_prompt(self, title: str, genre: str, target_length: int, theme: Optional[str] = None) -> str:
        """
        構建大綱提示
        
        參數:
            title (str): 小說標題
            genre (str): 小說類型
            target_length (int): 目標章節數
            theme (Optional[str]): 小說主題
            
        返回:
            str: 提示
        """
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
    
    def _build_chapter_structure_prompt(self, novel_outline: str, num_chapters: int) -> str:
        """
        構建章節結構提示
        
        參數:
            novel_outline (str): 小說大綱
            num_chapters (int): 章節數量
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following novel outline, create a detailed chapter-by-chapter structure for a {num_chapters}-chapter novel:
        
        Novel Outline:
        {novel_outline}
        
        For each chapter, provide:
        1. Chapter number and title
        2. Brief summary of the chapter's content
        3. Key events or revelations
        4. Character development points
        5. How the chapter advances the overall plot
        
        Ensure that the chapter structure follows a compelling narrative arc with proper pacing, building tension, and satisfying resolution.
        """
        
        return prompt
    
    def _build_story_arcs_prompt(self, novel_outline: str, main_characters: str) -> str:
        """
        構建故事弧提示
        
        參數:
            novel_outline (str): 小說大綱
            main_characters (str): 主要角色
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following novel outline and main characters, design detailed story arcs for the novel:
        
        Novel Outline:
        {novel_outline}
        
        Main Characters:
        {main_characters}
        
        For each major story arc, provide:
        1. Arc name and description
        2. Characters involved
        3. Beginning, middle, and end points
        4. Key turning points and revelations
        5. How the arc contributes to the overall narrative
        
        Include both main plot arcs and character development arcs, ensuring they interweave cohesively.
        """
        
        return prompt

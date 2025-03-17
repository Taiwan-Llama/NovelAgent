"""
章節撰寫代理模組 - 負責撰寫小說章節內容
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class ChapterWriterAgent(BaseAgent):
    """
    章節撰寫代理，負責撰寫小說章節內容
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化章節撰寫代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "Chapter Writer", llm_config)
        self.system_prompt = f"You are {name}, a professional novelist specializing in writing engaging and cohesive novel chapters. Your writing is vivid, character-driven, and maintains consistent pacing and tone."
    
    def write_chapter(self, chapter_outline: str, character_profiles: str, previous_chapter_summary: Optional[str] = None) -> str:
        """
        撰寫章節
        
        參數:
            chapter_outline (str): 章節大綱
            character_profiles (str): 角色檔案
            previous_chapter_summary (Optional[str]): 前一章節摘要
            
        返回:
            str: 章節內容
        """
        prompt = self._build_chapter_prompt(chapter_outline, character_profiles, previous_chapter_summary)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_chapter_summary(self, chapter_content: str) -> str:
        """
        創建章節摘要
        
        參數:
            chapter_content (str): 章節內容
            
        返回:
            str: 章節摘要
        """
        prompt = self._build_summary_prompt(chapter_content)
        return self.llm.generate(prompt, self.system_prompt)
    
    def revise_chapter(self, chapter_content: str, revision_notes: str) -> str:
        """
        修改章節
        
        參數:
            chapter_content (str): 章節內容
            revision_notes (str): 修改建議
            
        返回:
            str: 修改後的章節內容
        """
        prompt = self._build_revision_prompt(chapter_content, revision_notes)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_chapter_prompt(self, chapter_outline: str, character_profiles: str, previous_chapter_summary: Optional[str] = None) -> str:
        """
        構建章節提示
        
        參數:
            chapter_outline (str): 章節大綱
            character_profiles (str): 角色檔案
            previous_chapter_summary (Optional[str]): 前一章節摘要
            
        返回:
            str: 提示
        """
        prompt = f"""
        Write a complete novel chapter based on the following outline and character profiles:
        
        Chapter Outline:
        {chapter_outline}
        
        Character Profiles:
        {character_profiles}
        """
        
        if previous_chapter_summary:
            prompt += f"""
            Previous Chapter Summary:
            {previous_chapter_summary}
            
            Ensure continuity with the previous chapter while advancing the story.
            """
        
        prompt += """
        Guidelines for writing:
        1. Write a complete chapter of approximately 6,000 words
        2. Use vivid descriptions and engaging dialogue
        3. Show character thoughts and emotions rather than telling
        4. Maintain consistent character voices and personalities
        5. Include sensory details to bring scenes to life
        6. Balance action, dialogue, and description
        7. End the chapter with an appropriate hook or resolution
        
        Write the complete chapter text now.
        """
        
        return prompt
    
    def _build_summary_prompt(self, chapter_content: str) -> str:
        """
        構建摘要提示
        
        參數:
            chapter_content (str): 章節內容
            
        返回:
            str: 提示
        """
        prompt = f"""
        Create a comprehensive summary of the following chapter:
        
        Chapter Content:
        {chapter_content}
        
        Your summary should include:
        1. Main plot developments
        2. Character appearances and development
        3. Key dialogue or revelations
        4. Setting details introduced
        5. Any foreshadowing or setup for future chapters
        
        The summary should be detailed enough to serve as a reference for maintaining continuity in future chapters.
        """
        
        return prompt
    
    def _build_revision_prompt(self, chapter_content: str, revision_notes: str) -> str:
        """
        構建修改提示
        
        參數:
            chapter_content (str): 章節內容
            revision_notes (str): 修改建議
            
        返回:
            str: 提示
        """
        prompt = f"""
        Revise the following chapter based on the revision notes provided:
        
        Chapter Content:
        {chapter_content}
        
        Revision Notes:
        {revision_notes}
        
        Guidelines for revision:
        1. Address all issues mentioned in the revision notes
        2. Maintain the original style and tone
        3. Ensure the revised chapter flows naturally
        4. Preserve key plot points and character development
        5. Improve prose quality where possible
        
        Provide the complete revised chapter.
        """
        
        return prompt

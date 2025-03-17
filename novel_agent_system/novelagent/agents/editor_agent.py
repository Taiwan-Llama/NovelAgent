"""
編輯審校代理模組 - 負責審校和修改小說內容
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class EditorAgent(BaseAgent):
    """
    編輯審校代理，負責審校和修改小說內容
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化編輯審校代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "Editor", llm_config)
        self.system_prompt = f"You are {name}, a professional editor with expertise in fiction. Your job is to review and improve novel content, ensuring high quality, consistency, and engaging prose."
    
    def review_chapter(self, chapter_content: str, novel_style_guide: str) -> str:
        """
        審校章節
        
        參數:
            chapter_content (str): 章節內容
            novel_style_guide (str): 小說風格指南
            
        返回:
            str: 審校意見
        """
        prompt = self._build_review_prompt(chapter_content, novel_style_guide)
        return self.llm.generate(prompt, self.system_prompt)
    
    def improve_prose(self, text: str, style_notes: str) -> str:
        """
        改進文筆
        
        參數:
            text (str): 文本內容
            style_notes (str): 風格說明
            
        返回:
            str: 改進後的文本
        """
        prompt = self._build_improve_prose_prompt(text, style_notes)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_pacing(self, chapter_content: str, chapter_outline: str) -> str:
        """
        檢查節奏
        
        參數:
            chapter_content (str): 章節內容
            chapter_outline (str): 章節大綱
            
        返回:
            str: 節奏評估
        """
        prompt = self._build_pacing_prompt(chapter_content, chapter_outline)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_style_guide(self, sample_chapters: List[str], genre: str) -> str:
        """
        創建風格指南
        
        參數:
            sample_chapters (List[str]): 樣本章節
            genre (str): 小說類型
            
        返回:
            str: 風格指南
        """
        prompt = self._build_style_guide_prompt(sample_chapters, genre)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_review_prompt(self, chapter_content: str, novel_style_guide: str) -> str:
        """
        構建審校提示
        
        參數:
            chapter_content (str): 章節內容
            novel_style_guide (str): 小說風格指南
            
        返回:
            str: 提示
        """
        prompt = f"""
        Review the following novel chapter according to the style guide provided:
        
        Chapter Content:
        {chapter_content}
        
        Style Guide:
        {novel_style_guide}
        
        Provide a comprehensive review including:
        1. Overall assessment of quality and engagement
        2. Strengths of the chapter
        3. Areas for improvement
        4. Specific issues with prose, dialogue, or description
        5. Pacing and structure concerns
        6. Suggestions for revision
        
        Be constructive and specific in your feedback, providing examples where possible.
        """
        
        return prompt
    
    def _build_improve_prose_prompt(self, text: str, style_notes: str) -> str:
        """
        構建改進文筆提示
        
        參數:
            text (str): 文本內容
            style_notes (str): 風格說明
            
        返回:
            str: 提示
        """
        prompt = f"""
        Improve the following prose according to the style notes provided:
        
        Text:
        {text}
        
        Style Notes:
        {style_notes}
        
        Guidelines for improvement:
        1. Enhance vivid imagery and sensory details
        2. Vary sentence structure and rhythm
        3. Strengthen character voice and perspective
        4. Replace weak verbs and generic descriptions with more specific ones
        5. Eliminate unnecessary words and redundancies
        6. Maintain the original meaning and key plot points
        
        Provide the improved version of the text.
        """
        
        return prompt
    
    def _build_pacing_prompt(self, chapter_content: str, chapter_outline: str) -> str:
        """
        構建節奏提示
        
        參數:
            chapter_content (str): 章節內容
            chapter_outline (str): 章節大綱
            
        返回:
            str: 提示
        """
        prompt = f"""
        Analyze the pacing of the following chapter against its outline:
        
        Chapter Content:
        {chapter_content}
        
        Chapter Outline:
        {chapter_outline}
        
        In your analysis, address:
        1. Whether the chapter maintains appropriate pacing throughout
        2. If key events receive sufficient development and emphasis
        3. Areas where the narrative moves too quickly or too slowly
        4. Balance between action, dialogue, and description
        5. How well the chapter achieves its intended purpose from the outline
        6. Specific recommendations for pacing adjustments
        
        Provide a detailed assessment with examples from the text.
        """
        
        return prompt
    
    def _build_style_guide_prompt(self, sample_chapters: List[str], genre: str) -> str:
        """
        構建風格指南提示
        
        參數:
            sample_chapters (List[str]): 樣本章節
            genre (str): 小說類型
            
        返回:
            str: 提示
        """
        sample_text = "\n\n".join([f"Sample Chapter {i+1}:\n{chapter}" for i, chapter in enumerate(sample_chapters)])
        
        prompt = f"""
        Create a comprehensive style guide for a novel based on the following sample chapters and genre:
        
        Genre:
        {genre}
        
        {sample_text}
        
        Your style guide should include:
        1. Voice and tone guidelines
        2. Point of view and narrative perspective
        3. Dialogue style and formatting
        4. Description and imagery preferences
        5. Pacing and structure recommendations
        6. Language conventions specific to this novel
        7. Common themes and motifs to emphasize
        
        The style guide should be detailed enough to ensure consistency across multiple chapters while allowing for creative expression.
        """
        
        return prompt

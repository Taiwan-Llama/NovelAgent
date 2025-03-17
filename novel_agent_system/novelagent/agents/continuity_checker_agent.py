"""
連貫性檢查代理模組 - 負責檢查小說內容的連貫性和一致性
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class ContinuityCheckerAgent(BaseAgent):
    """
    連貫性檢查代理，負責檢查小說內容的連貫性和一致性
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化連貫性檢查代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "Continuity Checker", llm_config)
        self.system_prompt = f"You are {name}, a meticulous continuity editor for novels. Your job is to identify and resolve continuity errors, inconsistencies, and plot holes across chapters."
    
    def check_character_continuity(self, chapter_content: str, character_profiles: str, previous_chapters_summaries: List[str]) -> str:
        """
        檢查角色連貫性
        
        參數:
            chapter_content (str): 章節內容
            character_profiles (str): 角色檔案
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 角色連貫性檢查結果
        """
        prompt = self._build_character_continuity_prompt(chapter_content, character_profiles, previous_chapters_summaries)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_plot_continuity(self, chapter_content: str, novel_outline: str, previous_chapters_summaries: List[str]) -> str:
        """
        檢查情節連貫性
        
        參數:
            chapter_content (str): 章節內容
            novel_outline (str): 小說大綱
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 情節連貫性檢查結果
        """
        prompt = self._build_plot_continuity_prompt(chapter_content, novel_outline, previous_chapters_summaries)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_world_building_continuity(self, chapter_content: str, world_setting: str, previous_chapters_summaries: List[str]) -> str:
        """
        檢查世界觀連貫性
        
        參數:
            chapter_content (str): 章節內容
            world_setting (str): 世界設定
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 世界觀連貫性檢查結果
        """
        prompt = self._build_world_continuity_prompt(chapter_content, world_setting, previous_chapters_summaries)
        return self.llm.generate(prompt, self.system_prompt)
    
    def check_timeline_consistency(self, chapter_content: str, previous_chapters_summaries: List[str]) -> str:
        """
        檢查時間線一致性
        
        參數:
            chapter_content (str): 章節內容
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 時間線一致性檢查結果
        """
        prompt = self._build_timeline_prompt(chapter_content, previous_chapters_summaries)
        return self.llm.generate(prompt, self.system_prompt)
    
    def generate_continuity_notes(self, novel_outline: str, character_profiles: str, world_setting: str) -> str:
        """
        生成連貫性筆記
        
        參數:
            novel_outline (str): 小說大綱
            character_profiles (str): 角色檔案
            world_setting (str): 世界設定
            
        返回:
            str: 連貫性筆記
        """
        prompt = self._build_continuity_notes_prompt(novel_outline, character_profiles, world_setting)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_character_continuity_prompt(self, chapter_content: str, character_profiles: str, previous_chapters_summaries: List[str]) -> str:
        """
        構建角色連貫性提示
        
        參數:
            chapter_content (str): 章節內容
            character_profiles (str): 角色檔案
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 提示
        """
        summaries = "\n\n".join([f"Chapter {i+1} Summary:\n{summary}" for i, summary in enumerate(previous_chapters_summaries)])
        
        prompt = f"""
        Check the following chapter for character continuity issues against the character profiles and previous chapter summaries:
        
        Chapter Content:
        {chapter_content}
        
        Character Profiles:
        {character_profiles}
        
        Previous Chapters Summaries:
        {summaries}
        
        Identify any issues related to:
        1. Character personality inconsistencies
        2. Character knowledge or abilities that contradict earlier chapters
        3. Relationship dynamics that don't align with established patterns
        4. Character motivations that seem to shift without explanation
        5. Physical descriptions that don't match established character profiles
        
        For each issue found, provide:
        - The specific inconsistency
        - Where it appears in the current chapter
        - The contradicting information from previous chapters or profiles
        - A suggested correction
        
        If no issues are found, provide confirmation of character continuity.
        """
        
        return prompt
    
    def _build_plot_continuity_prompt(self, chapter_content: str, novel_outline: str, previous_chapters_summaries: List[str]) -> str:
        """
        構建情節連貫性提示
        
        參數:
            chapter_content (str): 章節內容
            novel_outline (str): 小說大綱
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 提示
        """
        summaries = "\n\n".join([f"Chapter {i+1} Summary:\n{summary}" for i, summary in enumerate(previous_chapters_summaries)])
        
        prompt = f"""
        Check the following chapter for plot continuity issues against the novel outline and previous chapter summaries:
        
        Chapter Content:
        {chapter_content}
        
        Novel Outline:
        {novel_outline}
        
        Previous Chapters Summaries:
        {summaries}
        
        Identify any issues related to:
        1. Plot events that contradict the established timeline
        2. Story elements that don't align with the novel outline
        3. Unresolved plot threads from previous chapters
        4. New plot elements that appear without proper setup
        5. Plot holes or logical inconsistencies
        
        For each issue found, provide:
        - The specific inconsistency
        - Where it appears in the current chapter
        - The contradicting information from previous chapters or the outline
        - A suggested correction
        
        If no issues are found, provide confirmation of plot continuity.
        """
        
        return prompt
    
    def _build_world_continuity_prompt(self, chapter_content: str, world_setting: str, previous_chapters_summaries: List[str]) -> str:
        """
        構建世界觀連貫性提示
        
        參數:
            chapter_content (str): 章節內容
            world_setting (str): 世界設定
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 提示
        """
        summaries = "\n\n".join([f"Chapter {i+1} Summary:\n{summary}" for i, summary in enumerate(previous_chapters_summaries)])
        
        prompt = f"""
        Check the following chapter for world-building continuity issues against the world setting and previous chapter summaries:
        
        Chapter Content:
        {chapter_content}
        
        World Setting:
        {world_setting}
        
        Previous Chapters Summaries:
        {summaries}
        
        Identify any issues related to:
        1. Geographic or location inconsistencies
        2. Cultural or societal elements that contradict established world-building
        3. Rules of magic, technology, or other systems that don't align with previous chapters
        4. Historical references that conflict with the established timeline
        5. Environmental or setting details that don't match the world setting
        
        For each issue found, provide:
        - The specific inconsistency
        - Where it appears in the current chapter
        - The contradicting information from previous chapters or the world setting
        - A suggested correction
        
        If no issues are found, provide confirmation of world-building continuity.
        """
        
        return prompt
    
    def _build_timeline_prompt(self, chapter_content: str, previous_chapters_summaries: List[str]) -> str:
        """
        構建時間線提示
        
        參數:
            chapter_content (str): 章節內容
            previous_chapters_summaries (List[str]): 前幾章摘要
            
        返回:
            str: 提示
        """
        summaries = "\n\n".join([f"Chapter {i+1} Summary:\n{summary}" for i, summary in enumerate(previous_chapters_summaries)])
        
        prompt = f"""
        Check the following chapter for timeline consistency issues against the previous chapter summaries:
        
        Chapter Content:
        {chapter_content}
        
        Previous Chapters Summaries:
        {summaries}
        
        Identify any issues related to:
        1. Time passage that doesn't align with previous chapters
        2. Events occurring out of sequence
        3. Character ages or time-dependent elements that don't match
        4. Seasonal or time-of-day inconsistencies
        5. References to past events with incorrect timing
        
        For each issue found, provide:
        - The specific inconsistency
        - Where it appears in the current chapter
        - The contradicting information from previous chapters
        - A suggested correction
        
        If no issues are found, provide confirmation of timeline consistency.
        """
        
        return prompt
    
    def _build_continuity_notes_prompt(self, novel_outline: str, character_profiles: str, world_setting: str) -> str:
        """
        構建連貫性筆記提示
        
        參數:
            novel_outline (str): 小說大綱
            character_profiles (str): 角色檔案
            world_setting (str): 世界設定
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following novel outline, character profiles, and world setting, create comprehensive continuity notes to guide the writing process:
        
        Novel Outline:
        {novel_outline}
        
        Character Profiles:
        {character_profiles}
        
        World Setting:
        {world_setting}
        
        Your continuity notes should include:
        1. Key timeline events and their chronological order
        2. Character relationship map and development trajectories
        3. Important world-building elements that must remain consistent
        4. Potential continuity challenges and how to address them
        5. Critical details that authors should track across chapters
        
        Create detailed notes that will serve as a reference to maintain consistency throughout the novel writing process.
        """
        
        return prompt

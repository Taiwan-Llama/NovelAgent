"""
角色設計代理模組 - 負責創建角色檔案和角色關係
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class CharacterDesignerAgent(BaseAgent):
    """
    角色設計代理，負責創建角色檔案和角色關係
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化角色設計代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "Character Designer", llm_config)
        self.system_prompt = f"You are {name}, a professional character designer for novels. Your job is to create detailed character profiles, design character relationships, and ensure consistent character development throughout the story."
    
    def create_character_profiles(self, novel_outline: str, num_main_characters: int, num_supporting_characters: int) -> str:
        """
        創建角色檔案
        
        參數:
            novel_outline (str): 小說大綱
            num_main_characters (int): 主要角色數量
            num_supporting_characters (int): 配角數量
            
        返回:
            str: 角色檔案
        """
        prompt = self._build_character_profiles_prompt(novel_outline, num_main_characters, num_supporting_characters)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_character_relationships(self, character_profiles: str) -> str:
        """
        設計角色關係
        
        參數:
            character_profiles (str): 角色檔案
            
        返回:
            str: 角色關係
        """
        prompt = self._build_character_relationships_prompt(character_profiles)
        return self.llm.generate(prompt, self.system_prompt)
    
    def plan_character_arcs(self, character_profiles: str, novel_outline: str) -> str:
        """
        規劃角色發展弧
        
        參數:
            character_profiles (str): 角色檔案
            novel_outline (str): 小說大綱
            
        返回:
            str: 角色發展弧
        """
        prompt = self._build_character_arcs_prompt(character_profiles, novel_outline)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_character_profiles_prompt(self, novel_outline: str, num_main_characters: int, num_supporting_characters: int) -> str:
        """
        構建角色檔案提示
        
        參數:
            novel_outline (str): 小說大綱
            num_main_characters (int): 主要角色數量
            num_supporting_characters (int): 配角數量
            
        返回:
            str: 提示
        """
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
    
    def _build_character_relationships_prompt(self, character_profiles: str) -> str:
        """
        構建角色關係提示
        
        參數:
            character_profiles (str): 角色檔案
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following character profiles, design a detailed relationship map showing how all characters are connected:
        
        Character Profiles:
        {character_profiles}
        
        For each significant relationship, provide:
        1. The nature of the relationship (family, friends, rivals, etc.)
        2. History of the relationship
        3. Current dynamics and tensions
        4. How the relationship might evolve throughout the story
        
        Create a complex web of relationships that will drive conflict and character development.
        """
        
        return prompt
    
    def _build_character_arcs_prompt(self, character_profiles: str, novel_outline: str) -> str:
        """
        構建角色發展弧提示
        
        參數:
            character_profiles (str): 角色檔案
            novel_outline (str): 小說大綱
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following character profiles and novel outline, design detailed character arcs for each main character:
        
        Character Profiles:
        {character_profiles}
        
        Novel Outline:
        {novel_outline}
        
        For each main character, outline their development arc including:
        1. Starting point (initial state, beliefs, flaws)
        2. Key turning points and challenges
        3. Internal and external conflicts
        4. Growth and change throughout the story
        5. Resolution and final state
        
        Ensure that each character's arc integrates meaningfully with the overall plot and themes.
        """
        
        return prompt

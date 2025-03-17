"""
世界觀設計代理模組 - 負責創建小說世界的設定和背景
"""

from typing import Dict, Any, List, Optional
from ..novelagent.base_agent import BaseAgent


class WorldBuildingAgent(BaseAgent):
    """
    世界觀設計代理，負責創建小說世界的設定和背景
    
    屬性:
        name (str): 代理名稱
        llm_config (Dict[str, Any]): LLM配置
    """
    
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        """
        初始化世界觀設計代理
        
        參數:
            name (str): 代理名稱
            llm_config (Dict[str, Any]): LLM配置
        """
        super().__init__(name, "World Builder", llm_config)
        self.system_prompt = f"You are {name}, a professional world-building expert for novels. Your job is to create detailed, consistent, and immersive fictional worlds with rich histories, cultures, and environments."
    
    def create_world_setting(self, novel_outline: str, genre: str) -> str:
        """
        創建世界設定
        
        參數:
            novel_outline (str): 小說大綱
            genre (str): 小說類型
            
        返回:
            str: 世界設定
        """
        prompt = self._build_world_setting_prompt(novel_outline, genre)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_locations(self, world_setting: str, num_locations: int) -> str:
        """
        設計地點
        
        參數:
            world_setting (str): 世界設定
            num_locations (int): 地點數量
            
        返回:
            str: 地點設計
        """
        prompt = self._build_locations_prompt(world_setting, num_locations)
        return self.llm.generate(prompt, self.system_prompt)
    
    def create_history_and_lore(self, world_setting: str) -> str:
        """
        創建歷史和傳說
        
        參數:
            world_setting (str): 世界設定
            
        返回:
            str: 歷史和傳說
        """
        prompt = self._build_history_lore_prompt(world_setting)
        return self.llm.generate(prompt, self.system_prompt)
    
    def design_cultures_and_societies(self, world_setting: str, num_cultures: int) -> str:
        """
        設計文化和社會
        
        參數:
            world_setting (str): 世界設定
            num_cultures (int): 文化數量
            
        返回:
            str: 文化和社會設計
        """
        prompt = self._build_cultures_prompt(world_setting, num_cultures)
        return self.llm.generate(prompt, self.system_prompt)
    
    def _build_world_setting_prompt(self, novel_outline: str, genre: str) -> str:
        """
        構建世界設定提示
        
        參數:
            novel_outline (str): 小說大綱
            genre (str): 小說類型
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following novel outline and genre, create a detailed world setting:
        
        Novel Outline:
        {novel_outline}
        
        Genre:
        {genre}
        
        Your world setting should include:
        1. The overall physical environment (geography, climate, etc.)
        2. The time period or technological level
        3. Major political or social structures
        4. Unique features that make this world distinctive
        5. Rules or systems (magic, technology, etc.) that operate in this world
        
        Create a rich, immersive, and internally consistent world that serves as an engaging backdrop for the story.
        """
        
        return prompt
    
    def _build_locations_prompt(self, world_setting: str, num_locations: int) -> str:
        """
        構建地點提示
        
        參數:
            world_setting (str): 世界設定
            num_locations (int): 地點數量
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following world setting, design {num_locations} key locations for the novel:
        
        World Setting:
        {world_setting}
        
        For each location, provide:
        1. Name and type of location (city, wilderness, building, etc.)
        2. Physical description and notable features
        3. Cultural or historical significance
        4. Current state and inhabitants
        5. Role in the story
        
        Create diverse and memorable locations that will enrich the narrative and provide interesting settings for key scenes.
        """
        
        return prompt
    
    def _build_history_lore_prompt(self, world_setting: str) -> str:
        """
        構建歷史和傳說提示
        
        參數:
            world_setting (str): 世界設定
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following world setting, create a rich history and lore for this fictional world:
        
        World Setting:
        {world_setting}
        
        Your history and lore should include:
        1. Timeline of major historical events
        2. Legendary figures or heroes
        3. Myths, religions, or belief systems
        4. Major conflicts or turning points
        5. How the past influences the present world
        
        Create a layered history that feels authentic and provides depth to the world, with elements that can be revealed throughout the story.
        """
        
        return prompt
    
    def _build_cultures_prompt(self, world_setting: str, num_cultures: int) -> str:
        """
        構建文化和社會提示
        
        參數:
            world_setting (str): 世界設定
            num_cultures (int): 文化數量
            
        返回:
            str: 提示
        """
        prompt = f"""
        Based on the following world setting, design {num_cultures} distinct cultures or societies:
        
        World Setting:
        {world_setting}
        
        For each culture or society, describe:
        1. Name and general location
        2. Social structure and governance
        3. Values, traditions, and customs
        4. Art, language, and cultural expressions
        5. Relationship with other cultures
        6. Unique aspects that make this culture distinctive
        
        Create diverse, believable cultures that add richness to the world and potential for interesting cultural interactions and conflicts.
        """
        
        return prompt

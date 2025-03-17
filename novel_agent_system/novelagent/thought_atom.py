"""
思想原子模組 - 實現思想原子和分層概括機制
"""

from typing import Dict, Any, List, Optional
from .llm_interface import LLMInterface


class ThoughtAtom:
    """
    思想原子，用於處理長上下文和分層概括
    
    屬性:
        content (str): 內容
        level (int): 層級
        parent (Optional[ThoughtAtom]): 父思想原子
        children (List[ThoughtAtom]): 子思想原子列表
        metadata (Dict[str, Any]): 元數據
    """
    
    def __init__(self, content: str, level: int = 0, parent: Optional['ThoughtAtom'] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        初始化思想原子
        
        參數:
            content (str): 內容
            level (int): 層級
            parent (Optional[ThoughtAtom]): 父思想原子
            metadata (Optional[Dict[str, Any]]): 元數據
        """
        self.content = content
        self.level = level
        self.parent = parent
        self.children = []
        self.metadata = metadata or {}
    
    def add_child(self, child: 'ThoughtAtom') -> None:
        """
        添加子思想原子
        
        參數:
            child (ThoughtAtom): 子思想原子
        """
        self.children.append(child)
        child.parent = self
        child.level = self.level + 1
    
    def summarize(self, llm_interface: LLMInterface) -> str:
        """
        總結當前思想原子及其子思想
        
        參數:
            llm_interface (LLMInterface): LLM接口
            
        返回:
            str: 總結
        """
        if not self.children:
            return self.content
        
        child_summaries = [child.summarize(llm_interface) for child in self.children]
        combined = "\n\n".join(child_summaries)
        
        # 使用LLM生成摘要
        prompt = f"""
        Summarize the following content into a coherent and comprehensive summary:
        
        {combined}
        
        Your summary should capture all key points while being more concise than the original.
        """
        
        summary = llm_interface.generate(prompt)
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """
        轉換為字典
        
        返回:
            Dict[str, Any]: 字典表示
        """
        return {
            "content": self.content,
            "level": self.level,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThoughtAtom':
        """
        從字典創建思想原子
        
        參數:
            data (Dict[str, Any]): 字典數據
            
        返回:
            ThoughtAtom: 思想原子
        """
        atom = cls(
            content=data["content"],
            level=data["level"],
            metadata=data.get("metadata", {})
        )
        
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data)
            atom.add_child(child)
        
        return atom
    
    def find_by_metadata(self, key: str, value: Any) -> List['ThoughtAtom']:
        """
        根據元數據查找思想原子
        
        參數:
            key (str): 元數據鍵
            value (Any): 元數據值
            
        返回:
            List[ThoughtAtom]: 匹配的思想原子列表
        """
        results = []
        
        if self.metadata.get(key) == value:
            results.append(self)
        
        for child in self.children:
            results.extend(child.find_by_metadata(key, value))
        
        return results
    
    def get_path(self) -> List[str]:
        """
        獲取從根到當前思想原子的路徑
        
        返回:
            List[str]: 路徑
        """
        if self.parent is None:
            return [self.content]
        else:
            return self.parent.get_path() + [self.content]
    
    def get_root(self) -> 'ThoughtAtom':
        """
        獲取根思想原子
        
        返回:
            ThoughtAtom: 根思想原子
        """
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()
    
    def __str__(self) -> str:
        """字符串表示"""
        indent = "  " * self.level
        return f"{indent}{self.content} (Level {self.level})"
    
    def __repr__(self) -> str:
        """表示形式"""
        return self.__str__()


class ThoughtTree:
    """
    思想樹，管理思想原子的層次結構
    
    屬性:
        root (ThoughtAtom): 根思想原子
        llm_interface (LLMInterface): LLM接口
    """
    
    def __init__(self, root_content: str, llm_config: Dict[str, Any]):
        """
        初始化思想樹
        
        參數:
            root_content (str): 根思想原子內容
            llm_config (Dict[str, Any]): LLM配置
        """
        self.root = ThoughtAtom(root_content)
        self.llm_interface = LLMInterface(llm_config)
    
    def add_thought(self, content: str, parent: Optional[ThoughtAtom] = None, metadata: Optional[Dict[str, Any]] = None) -> ThoughtAtom:
        """
        添加思想原子
        
        參數:
            content (str): 內容
            parent (Optional[ThoughtAtom]): 父思想原子，如果為None則添加到根
            metadata (Optional[Dict[str, Any]]): 元數據
            
        返回:
            ThoughtAtom: 添加的思想原子
        """
        parent = parent or self.root
        thought = ThoughtAtom(content, parent.level + 1, parent, metadata)
        parent.add_child(thought)
        return thought
    
    def summarize(self) -> str:
        """
        總結整個思想樹
        
        返回:
            str: 總結
        """
        return self.root.summarize(self.llm_interface)
    
    def find_by_metadata(self, key: str, value: Any) -> List[ThoughtAtom]:
        """
        根據元數據查找思想原子
        
        參數:
            key (str): 元數據鍵
            value (Any): 元數據值
            
        返回:
            List[ThoughtAtom]: 匹配的思想原子列表
        """
        return self.root.find_by_metadata(key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        轉換為字典
        
        返回:
            Dict[str, Any]: 字典表示
        """
        return self.root.to_dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], llm_config: Dict[str, Any]) -> 'ThoughtTree':
        """
        從字典創建思想樹
        
        參數:
            data (Dict[str, Any]): 字典數據
            llm_config (Dict[str, Any]): LLM配置
            
        返回:
            ThoughtTree: 思想樹
        """
        tree = cls("", llm_config)
        tree.root = ThoughtAtom.from_dict(data)
        return tree
    
    def print_tree(self) -> None:
        """打印思想樹"""
        self._print_node(self.root)
    
    def _print_node(self, node: ThoughtAtom, indent: int = 0) -> None:
        """
        打印節點
        
        參數:
            node (ThoughtAtom): 節點
            indent (int): 縮進
        """
        print("  " * indent + node.content)
        for child in node.children:
            self._print_node(child, indent + 1)

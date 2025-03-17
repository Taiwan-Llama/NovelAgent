#!/usr/bin/env python3
"""
NovelAgent 示例腳本 - 展示如何使用 NovelAgent 系統生成小說
"""

import os
import sys
import json
from pathlib import Path

# 添加項目根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from novelagent.agent_coordinator import AgentCoordinator
from novelagent.task_manager import TaskManager
from novelagent.agents.novel_planner_agent import NovelPlannerAgent
from novelagent.agents.character_designer_agent import CharacterDesignerAgent
from novelagent.agents.world_building_agent import WorldBuildingAgent
from novelagent.agents.chapter_writer_agent import ChapterWriterAgent
from novelagent.agents.editor_agent import EditorAgent
from novelagent.agents.continuity_checker_agent import ContinuityCheckerAgent


def save_to_file(content, filename):
    """保存內容到文件"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已保存到文件: {filename}")


def main():
    """主函數"""
    print("NovelAgent 示例 - 小說生成系統")
    
    # 配置 LLM
    # 注意: 請替換為您自己的 API 密鑰
    llm_config = {
        "model": "gpt-4",
        "api_key": "your_api_key_here",
        "temperature": 0.7
    }
    
    # 創建代理
    print("創建專業化代理...")
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
    
    # 設置小說參數
    novel_title = "魔法世界的冒險"
    genre = "奇幻"
    target_length = 5  # 示例中僅生成 5 章
    
    # 添加小說生成任務
    print("設置小說生成任務...")
    task_manager.add_task("create_outline", "創建小說大綱", {"assigned_to": "Planner"})
    task_manager.add_task("create_chapter_structure", "創建章節結構", {"assigned_to": "Planner", "depends_on": "create_outline"})
    task_manager.add_task("design_characters", "設計角色", {"assigned_to": "CharacterDesigner", "depends_on": "create_outline"})
    task_manager.add_task("design_world", "設計世界觀", {"assigned_to": "WorldBuilder", "depends_on": "create_outline"})
    task_manager.add_task("create_continuity_notes", "創建連貫性筆記", {"assigned_to": "ContinuityChecker", "depends_on": "design_characters,design_world"})
    
    # 模擬小說生成流程
    print("\n開始小說生成流程...")
    
    # 創建小說目錄
    novel_dir = f"./novels/{novel_title}"
    os.makedirs(novel_dir, exist_ok=True)
    
    # 創建小說大綱
    print("1. 創建小說大綱...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # novel_outline = agent.create_novel_outline(novel_title, genre, target_length)
    
    # 示例大綱（模擬生成結果）
    novel_outline = """
    # 魔法世界的冒險
    
    ## 核心前提
    在一個充滿魔法的世界中，一位普通農家少年小明意外發現了一本古老的魔法書，獲得了控制火焰的能力。他被魔法學院招募，開始了一段非凡的冒險，最終揭露了威脅整個王國的黑暗陰謀。
    
    ## 主要衝突
    小明必須在學習控制自己新獲得的魔法能力的同時，對抗一個秘密組織，該組織試圖喚醒一個遠古的黑暗力量來統治王國。
    
    ## 設定與世界觀
    故事發生在一個魔法與科技共存的世界，魔法被分為五大元素：火、水、土、風、雷。魔法學院是培養魔法師的最高學府，位於王國首都。
    
    ## 敘事結構
    故事遵循英雄之旅的結構，從小明的平凡生活開始，經歷召喚冒險、試煉、獲得盟友、面對敵人，最終成長為一名強大的魔法師。
    
    ## 關鍵情節點
    1. 小明發現魔法書並獲得火焰魔法能力
    2. 小明被魔法學院招募
    3. 小明在學院結交朋友並發現自己的特殊天賦
    4. 小明發現秘密組織的存在
    5. 小明與朋友們揭露並阻止秘密組織的陰謀
    """
    
    save_to_file(novel_outline, f"{novel_dir}/outline.md")
    task_manager.complete_task(current_task["id"])
    
    # 創建章節結構
    print("2. 創建章節結構...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # chapter_structure = agent.create_chapter_structure(novel_outline, target_length)
    
    # 示例章節結構（模擬生成結果）
    chapter_structure = """
    # 魔法世界的冒險 - 章節結構
    
    ## 第1章：神秘的魔法書
    小明在森林中發現了一個神秘的洞穴，裡面有一本古老的魔法書。他帶回家後開始閱讀，意外釋放出火焰，驚訝地發現自己擁有了魔法能力。
    
    ## 第2章：初試魔法
    小明開始學習魔法書中的咒語，發現自己擁有了控制火焰的能力。他在練習過程中引起了村民的注意，包括村長的女兒小紅。
    
    ## 第3章：魔法學院的邀請
    小明的能力引起了魔法學院的注意，一位名叫李教授的魔法師來到村子，邀請小明加入魔法學院學習。小明告別家人和小紅，踏上了前往首都的旅程。
    
    ## 第4章：初入學院
    小明抵達魔法學院，被分配到火系班級。他結識了室友小藍（水系魔法師）和小綠（風系魔法師），開始適應學院生活。
    
    ## 第5章：神秘事件
    學院內開始發生一系列神秘事件，有學生報告看到黑影在夜間活動。小明和朋友們決定調查，發現了一個秘密組織的蹤跡。
    """
    
    save_to_file(chapter_structure, f"{novel_dir}/chapter_structure.md")
    task_manager.complete_task(current_task["id"])
    
    # 設計角色
    print("3. 設計角色...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # character_profiles = agent.create_character_profiles(novel_outline, 3, 5)
    
    # 示例角色檔案（模擬生成結果）
    character_profiles = """
    # 魔法世界的冒險 - 角色檔案
    
    ## 主要角色
    
    ### 小明
    - 年齡：17歲
    - 外貌：黑髮褐眼，身材偏瘦但結實，臉上總帶著好奇的表情
    - 背景：出身於邊境小村的普通農家，父母是農民
    - 性格：好奇心強，勇敢，正直，有時衝動
    - 目標：掌握火焰魔法，保護家人和朋友
    - 衝突：控制自己的魔法能力，對抗黑暗勢力
    - 角色弧：從懵懂少年成長為負責任的魔法師
    
    ### 小藍
    - 年齡：18歲
    - 外貌：藍色短髮，藍眼睛，身材修長
    - 背景：來自沿海城市的商人家庭
    - 性格：冷靜，理性，細心，有時過於謹慎
    - 目標：成為一名治療師
    - 衝突：克服對自己能力的懷疑
    - 角色弧：從自我懷疑到自信滿滿
    
    ### 小綠
    - 年齡：16歲
    - 外貌：綠色長髮，綠眼睛，嬌小靈活
    - 背景：森林部落的後裔，與自然有特殊聯繫
    - 性格：活潑，直率，樂觀，有時魯莽
    - 目標：探索世界，了解自己的部落歷史
    - 衝突：在現代社會和傳統文化之間尋找平衡
    - 角色弧：從叛逆少女到文化傳承者
    
    ## 配角
    
    ### 李教授
    - 年齡：45歲
    - 外貌：灰白頭髮，戴眼鏡，穿著整潔的魔法長袍
    - 背景：魔法學院資深教授，火系魔法專家
    - 性格：嚴厲但公正，關心學生
    - 角色作用：小明的導師和引路人
    
    ### 小紅
    - 年齡：17歲
    - 外貌：紅色長髮，棕色眼睛，臉上有雀斑
    - 背景：村長的女兒，小明的青梅竹馬
    - 性格：堅強，實際，有領導能力
    - 角色作用：小明的情感聯繫和動力來源
    
    ### 黑袍首領
    - 年齡：不詳
    - 外貌：總是穿著黑色長袍，面容隱藏在陰影中
    - 背景：秘密組織的領導者，追求遠古黑暗力量
    - 性格：冷酷，野心勃勃，不擇手段
    - 角色作用：主要反派，代表小明必須克服的黑暗面
    
    ### 院長
    - 年齡：70歲
    - 外貌：白髮白鬍子，藍色眼睛炯炯有神
    - 背景：魔法學院的創始人之一
    - 性格：智慧，幽默，深謀遠慮
    - 角色作用：提供指導和關鍵信息
    
    ### 小黃
    - 年齡：18歲
    - 外貌：金黃色頭髮，琥珀色眼睛，高大強壯
    - 背景：貴族家庭出身
    - 性格：驕傲，好勝，但有正義感
    - 角色作用：初期的對手，後來的盟友
    """
    
    save_to_file(character_profiles, f"{novel_dir}/character_profiles.md")
    task_manager.complete_task(current_task["id"])
    
    # 設計世界觀
    print("4. 設計世界觀...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # world_setting = agent.create_world_setting(novel_outline, genre)
    
    # 示例世界設定（模擬生成結果）
    world_setting = """
    # 魔法世界的冒險 - 世界設定
    
    ## 物理環境
    
    ### 地理
    故事發生在艾爾法大陸，一個被四大海洋環繞的大陸。大陸分為五大區域，每個區域與一種元素魔法相對應：
    - 北方的火焰山脈：火元素魔法盛行的區域，多火山和溫泉
    - 東方的碧波海岸：水元素魔法盛行的區域，多湖泊和河流
    - 南方的翠綠森林：風元素魔法盛行的區域，多茂密森林和草原
    - 西方的石岩高地：土元素魔法盛行的區域，多山脈和峽谷
    - 中央的雷霆平原：雷元素魔法盛行的區域，多平原和丘陵
    
    ### 氣候
    大陸氣候多樣，從北方的寒冷到南方的溫暖，每個區域的氣候都受到當地主導元素魔法的影響。
    
    ## 時代與科技
    
    故事設定在一個魔法與科技共存的世界，相當於地球的中世紀晚期到文藝復興早期的科技水平，但因為魔法的存在，某些領域（如醫療、交通）的發展超前。
    
    主要交通工具包括馬車、帆船，以及魔法驅動的飛行器（僅限貴族和高級魔法師使用）。
    
    ## 政治與社會結構
    
    ### 政治體系
    艾爾法大陸由五大王國組成，每個王國對應一個元素區域：
    - 火焰王國：君主制，以軍事力量著稱
    - 碧波王國：議會制，以商業和航海著稱
    - 翠綠王國：部落聯盟，以農業和藥草學著稱
    - 石岩王國：寡頭制，以採礦和鍛造著稱
    - 雷霆王國：君主立憲制，以魔法研究著稱
    
    故事主要發生在雷霆王國，首都為魔法之都「雷文城」，魔法學院就位於此地。
    
    ### 社會階層
    社會分為貴族、平民和魔法師階層。魔法師擁有特殊地位，不受傳統階級限制，一個平民出身的強大魔法師可以獲得與貴族同等的尊重和權力。
    
    ## 魔法系統
    
    ### 元素魔法
    魔法分為五大元素：火、水、風、土、雷。每個人天生親和某種元素，但通過學習可以掌握其他元素魔法，雖然難度較大。
    
    ### 魔法學習
    魔法能力部分是天生的（魔法天賦），部分是後天學習的。魔法學院是正規學習魔法的場所，分為五大學院，對應五大元素。
    
    ### 魔法物品
    魔法書、魔法杖、魔法寶石等魔法物品可以增強或輔助施法者的能力。小明發現的古老魔法書是一件特別強大的魔法物品，據說是遠古時代偉大魔法師的遺物。
    
    ## 獨特特徵
    
    ### 魔法生物
    世界中存在各種魔法生物，如火龍、水精靈、風鷹、土熊和雷鳥等，它們都與特定元素有關。
    
    ### 元素節點
    大陸上分布著元素節點，是元素魔法能量特別集中的地方。魔法師可以在這些地方更容易地施展強大魔法。
    
    ### 魔法季節
    一年分為五季，每季節一種元素魔法特別強大。在特定季節，相應元素的魔法師能力會增強。
    
    ## 歷史背景
    
    千年前，艾爾法大陸經歷了一場魔法大戰，導致第六種元素「暗影」被封印。傳說中，秘密組織「暗影之手」一直試圖解開封印，釋放暗影元素的力量。
    """
    
    save_to_file(world_setting, f"{novel_dir}/world_setting.md")
    task_manager.complete_task(current_task["id"])
    
    # 創建連貫性筆記
    print("5. 創建連貫性筆記...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # continuity_notes = agent.generate_continuity_notes(novel_outline, character_profiles, world_setting)
    
    # 示例連貫性筆記（模擬生成結果）
    continuity_notes = """
    # 魔法世界的冒險 - 連貫性筆記
    
    ## 時間線
    
    ### 前史
    - 1000年前：魔法大戰，暗影元素被封印
    - 500年前：五大王國建立
    - 100年前：魔法學院成立
    
    ### 主要故事時間線
    - 第1章：小明發現魔法書（春季初）
    - 第2章：小明學習控制能力（春季中）
    - 第3章：小明被邀請加入學院（春季末）
    - 第4章：小明抵達學院，開始學習（夏季初）
    - 第5章：學院內發生神秘事件（夏季中）
    
    ## 角色關係圖
    
    ### 小明的關係
    - 小明 → 小紅：青梅竹馬，有感情
    - 小明 → 小藍：室友，朋友
    - 小明 → 小綠：室友，朋友
    - 小明 → 李教授：學生與導師
    - 小明 → 小黃：初期對手，後期盟友
    
    ### 其他關係
    - 小藍 → 小綠：好友
    - 李教授 → 院長：同事，尊敬
    - 黑袍首領 → 暗影之手：領導者
    
    ## 重要物品追蹤
    
    - 古老魔法書：小明在第1章發現，始終由他保管
    - 火焰寶石：將在後續章節出現，增強火系魔法
    - 學院徽章：所有學生都有，用於識別身份
    
    ## 魔法能力發展
    
    ### 小明的能力
    - 第1章：意外釋放火焰
    - 第2章：學會基本控制
    - 第3章：能夠有意識地施放小型火焰
    - 第4章：開始正式學習火系魔法理論
    - 第5章：學會第一個正式的火系魔法咒語
    
    ## 情節線索
    
    ### 主線：暗影之手的陰謀
    - 第1章：魔法書上有暗影之手的隱藏標記（伏筆）
    - 第5章：學院的神秘事件與暗影之手有關
    
    ### 支線：小明的身世之謎
    - 暗示小明的父母知道更多關於他身世的信息
    - 李教授似乎認識小明的父母
    
    ## 世界設定一致性
    
    ### 魔法規則
    - 元素親和力決定學習難度
    - 魔法需要咒語和手勢
    - 強大魔法需要魔法材料作為媒介
    - 過度使用魔法會導致疲勞
    
    ### 地理位置
    - 小明的村莊位於火焰山脈和雷霆平原之間
    - 魔法學院位於雷文城中心
    - 暗影之手的秘密基地位於學院地下
    
    ## 潛在連貫性問題
    
    - 確保小明的魔法能力發展合理，不要過快成長
    - 保持學院規則的一致性
    - 確保時間流逝與季節變化相符
    - 角色知識應與其背景和經歷相符
    """
    
    save_to_file(continuity_notes, f"{novel_dir}/continuity_notes.md")
    task_manager.complete_task(current_task["id"])
    
    # 為每章添加任務
    for i in range(1, target_length + 1):
        task_manager.add_task(f"write_chapter_{i}", f"撰寫第{i}章", {"assigned_to": "ChapterWriter", "depends_on": "create_continuity_notes" if i == 1 else f"check_continuity_chapter_{i-1}"})
        task_manager.add_task(f"review_chapter_{i}", f"審校第{i}章", {"assigned_to": "Editor", "depends_on": f"write_chapter_{i}"})
        task_manager.add_task(f"check_continuity_chapter_{i}", f"檢查第{i}章連貫性", {"assigned_to": "ContinuityChecker", "depends_on": f"review_chapter_{i}"})
    
    # 生成第一章（示例）
    print("\n6. 生成第一章...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # chapter_outline = chapter_structure.split("第1章：")[1].split("第2章：")[0]
    # chapter_content = agent.write_chapter(chapter_outline, character_profiles, None)
    
    # 示例章節內容（模擬生成結果）
    chapter_content = """
    # 第1章：神秘的魔法書
    
    春日的陽光溫暖地灑在邊境小村的田野上，小明擦了擦額頭上的汗水，直起腰來。他已經在田裡幫父母干了一上午的活，現在終於可以休息一會兒了。遠處，村子的輪廓在陽光下顯得格外寧靜。
    
    "小明！"一個清脆的聲音從村子方向傳來。小明轉頭，看見一頭紅髮在陽光下格外耀眼。那是村長的女兒小紅，他的青梅竹馬。
    
    "今天又要去森林嗎？"小紅走近後問道，她的棕色眼睛閃爍著好奇的光芒。
    
    小明點點頭，露出了期待的笑容。"聽說北邊的森林深處有個奇怪的洞穴，我想去看看。"
    
    "又是你的冒險。"小紅嘆了口氣，但眼中卻帶著羨慕，"我得幫媽媽準備晚餐，不能陪你去了。小心點，天黑前回來。"
    
    小明答應著，拿起放在田埂上的水壺和小包，向北方的森林走去。這片森林他已經探索了無數次，但總有新的角落等著他發現。這是他為數不多的樂趣——在平凡的農家生活中尋找一絲不平凡。
    
    森林比他想像的更加茂密。陽光透過樹葉間的縫隙，在地面上形成斑駁的光影。小明熟練地在樹木間穿行，偶爾停下來辨認方向。他從未走得這麼遠，但內心的好奇驅使他繼續前進。
    
    就在他準備休息時，一道奇怪的藍光從遠處閃過。小明眨了眨眼，以為是錯覺，但那光芒再次出現，若隱若現地在樹木間閃爍。
    
    "這是什麼？"小明自言自語，不由自主地向光源走去。
    
    穿過一片灌木叢後，小明發現自己站在一個小山坡前。山坡上有一個洞口，藍光正是從那裡發出的。洞口不大，剛好能容一個人彎腰進入。
    
    小明猶豫了一下。父母總告誡他不要冒險，但那神秘的藍光像是在呼喚他。最終，好奇心戰勝了謹慎，他彎下腰，鑽進了洞穴。
    
    洞內出乎意料地寬敞，藍光似乎來自洞穴深處。小明小心翼翼地前進，手扶著潮濕的石壁。隨著深入，藍光越來越亮，最終他來到了一個圓形的石室。
    
    石室中央有一個石台，上面放著一本厚重的書籍。正是這本書發出了神秘的藍光。書的封面上刻著奇怪的符文，在藍光的照耀下顯得古老而神秘。
    
    小明屏住呼吸，慢慢走近。他從未見過這樣的書，也不認識封面上的符文。出於本能，他伸出手，輕輕觸碰了書的封面。
    
    就在他的手指接觸到書的那一刻，藍光突然變得刺眼，整個石室都被照亮。小明感到一陣眩暈，但他沒有退縮，而是用雙手捧起了那本書。
    
    書比他想像的要輕，彷彿失去了重量。藍光漸漸減弱，最終只在書的邊緣閃爍。小明深吸一口氣，小心翼翼地打開了書。
    
    書頁上是他從未見過的文字和圖案，似乎是某種咒語和魔法陣。雖然不認識這些文字，但小明卻奇怪地感到一種親切感，彷彿他曾經認識這些符號。
    
    "這是什麼書？"小明輕聲問道，手指輕撫過書頁。
    
    就在這時，書頁上的一個符文突然亮了起來，一股暖流從書中湧出，順著小明的手指流入他的身體。他感到一陣溫暖，接著是一種前所未有的力量感。
    
    "啊！"小明驚呼一聲，本能地後退了一步。
    
    就在這一刻，他的手指尖突然冒出了一小撮火焰。火焰不燙，反而給人一種溫暖的感覺。小明驚訝地看著自己的手指，火焰隨著他的心跳跳動著，彷彿已經成為他身體的一部分。
    
    "這...這是魔法嗎？"小明難以置信地看著手中的火焰。
    
    火焰在他的控制下忽大忽小，最終在他的意念下熄滅。小明看了看手中的書，又看了看自己的手指，心中充滿了疑問和興奮。
    
    他決定帶走這本書。不管它是什麼，它已經改變了他的生活。小明小心地將書放入背包，走出洞穴。外面，夕陽已經西沉，他必須趕在天黑前回到村子。
    
    回家的路上，小明的腦海中充滿了問題。這本書是什麼？為什麼他能使用魔法？這意味著什麼？他決定暫時保守這個秘密，直到他弄清楚發生了什麼。
    
    當他回到村子時，夜幕已經降臨。小紅站在村口等他，臉上帶著擔憂。
    
    "你去哪了？我都要去找你了！"小紅責備道。
    
    小明笑了笑，沒有提及洞穴和書的事。"迷路了，抱歉讓你擔心。"
    
    小紅狐疑地看了他一眼，但沒有追問。"快回家吧，你父母在等你。"
    
    回到家中，小明匆匆吃過晚飯，便回到自己的小房間。他鎖上門，從背包中取出那本神秘的書。
    
    在油燈的微光下，書不再發出藍光，但封面上的符文依然清晰可見。小明深吸一口氣，再次打開了書。
    
    這一次，他試著集中注意力，希望能理解書中的內容。奇怪的是，雖然文字依然陌生，但他似乎能夠感受到其中的含義。第一頁似乎是關於火焰魔法的基礎知識。
    
    小明按照書中的指示，集中精神，想像火焰在他的掌心燃起。令他驚訝的是，一小撮火焰真的在他的手掌中出現了。
    
    "我真的會魔法了！"小明驚喜地低聲說道。
    
    他嘗試著控制火焰的大小和形狀，發現自己確實能夠通過意念來操控它。這種感覺既陌生又奇妙，彷彿他生來就應該擁有這種能力。
    
    小明沉浸在魔法的世界中，直到深夜才依依不捨地合上書。他將書小心地藏在床下的一個木箱中，躺在床上，腦海中充滿了對未來的想像。
    
    他不知道的是，這本古老的魔法書將徹底改變他的命運，帶他進入一個充滿魔法和冒險的世界。而在書的封底，一個幾乎看不見的暗影標記悄然閃爍，預示著更大的秘密等待揭露。
    
    夜深了，小明帶著對新發現的興奮沉沉睡去，夢中全是跳動的火焰和神秘的符文。
    """
    
    save_to_file(chapter_content, f"{novel_dir}/chapter_1.txt")
    task_manager.complete_task(current_task["id"])
    
    # 審校第一章（示例）
    print("7. 審校第一章...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # novel_style_guide = "保持輕快的敘事節奏，使用生動的描述和自然的對話。"
    # review_notes = agent.review_chapter(chapter_content, novel_style_guide)
    
    # 示例審校意見（模擬生成結果）
    review_notes = """
    # 第1章審校意見
    
    ## 整體評估
    
    章節整體質量良好，成功建立了故事的基礎設定和主角的初始狀態。敘事流暢，情節發展合理，為後續章節做了良好的鋪墊。
    
    ## 優點
    
    1. 人物形象鮮明，小明的好奇心和冒險精神刻畫得當
    2. 場景描寫生動，特別是森林和洞穴的氛圍營造成功
    3. 魔法元素的引入自然，不突兀
    4. 結尾埋下了伏筆，為後續情節發展做了鋪墊
    
    ## 需要改進的地方
    
    1. 小明發現魔法書的過程可以更加曲折，增加一些障礙或挑戰
    2. 小明對獲得魔法能力的反應可以更加豐富，包括驚訝、興奮、恐懼等複雜情緒
    3. 可以增加更多關於村莊和小明家庭的描述，豐富背景設定
    4. 對話部分可以再自然一些，增加口語化的表達
    
    ## 具體修改建議
    
    1. 第3段：可以增加小明與小紅的對話，展示他們的友情和小明的性格
    2. 第12段：描述小明觸碰魔法書時的感受可以更加詳細
    3. 第18段：小明使用火焰魔法的場景可以更加生動，描述他的情緒變化
    4. 結尾部分：可以暗示小明的特殊身世，增加懸念
    
    整體而言，這是一個很好的開篇章節，只需要小幅調整就能更加完善。
    """
    
    save_to_file(review_notes, f"{novel_dir}/chapter_1_review.txt")
    task_manager.complete_task(current_task["id"])
    
    # 檢查第一章連貫性（示例）
    print("8. 檢查第一章連貫性...")
    current_task = task_manager.get_next_task()
    agent = coordinator.get_agent(current_task["metadata"]["assigned_to"])
    
    # 注意: 在實際使用時，取消下面的註釋並使用真實的 API 調用
    # continuity_issues = agent.check_character_continuity(chapter_content, character_profiles, [])
    
    # 示例連貫性檢查結果（模擬生成結果）
    continuity_issues = """
    # 第1章連貫性檢查
    
    ## 角色連貫性
    
    - 小明的性格表現與角色檔案一致，好奇心強，勇敢
    - 小紅的描述與角色檔案一致，作為村長的女兒和小明的青梅竹馬
    - 小明的父母在章節中只是簡單提及，符合背景設定
    
    ## 情節連貫性
    
    - 章節內容與大綱描述一致，小明在森林中發現魔法書並獲得火焰魔法能力
    - 情節發展符合邏輯，從發現洞穴到獲得魔法能力的過程合理
    - 章節結尾為後續情節做了鋪墊，符合整體故事弧
    
    ## 世界觀連貫性
    
    - 村莊和森林的描述與世界設定相符
    - 魔法書和火焰魔法的描述符合魔法系統設定
    - 暗影標記的提及與世界歷史背景（暗影之手組織）相符
    
    ## 時間線一致性
    
    - 章節發生在春季初，符合時間線設定
    - 一天內的時間流逝描述合理，從上午到深夜
    
    ## 小問題
    
    1. 小明在角色檔案中描述為17歲，但章節中沒有明確提及他的年齡
    2. 魔法書在世界設定中應該有更具體的來源說明
    3. 可以增加一些關於村莊位置的描述，明確其位於火焰山脈和雷霆平原之間
    
    ## 建議修正
    
    1. 在適當位置加入小明年齡的提示
    2. 在小明研究魔法書時，可以暗示其可能的來源
    3. 增加一些關於遠處火焰山脈或雷霆平原的描述，建立地理感
    
    整體而言，第1章在連貫性方面表現良好，只需要小幅調整即可。
    """
    
    save_to_file(continuity_issues, f"{novel_dir}/chapter_1_continuity.txt")
    task_manager.complete_task(current_task["id"])
    
    # 創建章節摘要（示例）
    chapter_summary = """
    # 第1章摘要：神秘的魔法書
    
    ## 主要情節
    
    17歲的農家少年小明在北方森林深處發現了一個發出藍光的神秘洞穴。在洞穴中，他找到了一本古老的魔法書。當他觸碰書本時，獲得了控制火焰的魔法能力。小明帶著書回到村子，開始學習控制自己的新能力。
    
    ## 角色出場
    
    - 小明：主角，17歲農家少年，好奇心強，發現魔法書並獲得火焰魔法能力
    - 小紅：村長的女兒，小明的青梅竹馬，關心小明的安全
    - 小明的父母：簡單提及，沒有直接出場
    
    ## 關鍵對話/揭示
    
    - 小明與小紅的對話揭示了小明喜歡冒險的性格
    - 小明發現自己能夠控制火焰，確認獲得了魔法能力
    
    ## 場景設定
    
    - 邊境小村：小明的家鄉，平靜的農業社區
    - 北方森林：茂密神秘，隱藏著魔法洞穴
    - 魔法洞穴：發出藍光，內有圓形石室和石台
    - 小明的房間：他第一次嘗試控制火焰魔法的地方
    
    ## 伏筆/未來章節設置
    
    - 古老的魔法書：將成為小明學習魔法的關鍵
    - 書封底的暗影標記：暗示與暗影之手組織的聯繫
    - 小明對魔法的親和力：暗示他可能有特殊的身世
    
    ## 章節結束狀態
    
    小明成功獲得火焰魔法能力，決定保守這個秘密，開始自學魔法。他不知道這本書將徹底改變他的命運，帶他進入一個充滿魔法和冒險的世界。
    """
    
    save_to_file(chapter_summary, f"{novel_dir}/chapter_1_summary.txt")
    
    # 模擬生成其他章節（實際使用時會生成所有章節）
    print("\n已完成示例小說的前期生成。在實際使用中，系統會繼續生成所有章節。")
    print(f"\n所有文件已保存到目錄: {novel_dir}")
    
    # 列出生成的文件
    print("\n生成的文件列表:")
    for file in os.listdir(novel_dir):
        print(f"- {file}")


if __name__ == "__main__":
    main()

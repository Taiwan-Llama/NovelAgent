# 多智能體框架研究筆記

## 需求分析

用戶要求建立一個基於Python的多智能體系統，用於生成長篇小說，主要特點包括：

1. 使用LiteLLM的API和新設計的agent框架
2. 高度模組化設計
3. 能夠克服模型上下文限制，生成連貫的長篇小說（300+章，每章6000+字）
4. 使用PostgreSQL向量資料庫進行知識管理
5. 實現長上下文的分層概括
6. 支持任何LiteLLM支持的模型
7. 使用Ollama的嵌入API進行嵌入
8. 以AI團隊形式設計，個別維護上下文
9. 核心哲學：Code = SOP(Team)
10. 系統生成的小說保存在標題名稱下的資料夾，每個章節保存在單獨的txt中

## 現有框架分析

### SmolaGent框架

SmolaGent是Hugging Face開發的一個輕量級代理框架，其核心特點包括：

1. **簡潔性**：代理邏輯約1,000行程式碼，保持最小抽象形式
2. **模組化**：將代理功能分解為可組合的模組
3. **工具使用**：支持代理使用各種工具來完成任務
4. **靈活性**：可以與不同的LLM後端集成

SmolaGent的主要優勢在於其簡潔的設計和靈活的架構，但在處理長上下文和多代理協作方面可能存在局限。

### ReAct框架

ReAct (Reasoning and Acting) 是一種結合推理和行動的代理框架，其核心特點包括：

1. **思考-行動循環**：代理先進行推理，然後基於推理結果採取行動
2. **自我反思**：能夠評估自己的行動結果並調整策略
3. **工具使用**：能夠使用外部工具來獲取信息或執行操作
4. **上下文管理**：維護推理和行動的歷史記錄

ReAct框架在處理複雜任務時表現良好，但可能在處理超長內容生成時面臨上下文限制。

## 相關論文研究

### Self-Supervised Prompt Optimization

這篇論文提出了一種自監督的提示優化方法，主要思想包括：

1. **提示自優化**：代理能夠根據任務反饋自動優化自己的提示
2. **元學習**：通過學習如何生成更好的提示來提高性能
3. **自我評估**：代理能夠評估自己的輸出質量並進行調整

這一方法對於提高代理的生成質量和適應性非常有價值，可以應用於小說生成系統中的提示設計。

### Atom of Thoughts for Markov LLM Test-Time Scaling

這篇論文提出了"思想原子"的概念，主要思想包括：

1. **思想分解**：將複雜思考過程分解為更小的"思想原子"
2. **馬爾可夫鏈**：將思考過程視為馬爾可夫鏈，每個思想原子依賴於前一個
3. **測試時擴展**：在推理階段擴展模型的思考能力
4. **長上下文處理**：通過思想原子的組合處理長上下文任務

這一方法對於處理長篇小說的生成特別有價值，可以幫助我們設計分層的思考和生成過程。

### Executable Code Actions Elicit Better LLM Agents

這篇論文強調了可執行代碼操作在代理系統中的重要性，主要思想包括：

1. **代碼即行動**：使用可執行代碼作為代理的行動方式
2. **明確性**：代碼操作比自然語言指令更明確
3. **可驗證性**：代碼操作的結果可以直接驗證
4. **可組合性**：代碼操作可以組合成更複雜的行動

這一方法對於設計代理間的通信和協作機制非常有價值，可以應用於多代理系統的設計中。

## 現有框架的優缺點分析

### 優點

1. **模組化設計**：現有框架普遍採用模組化設計，便於擴展和維護
2. **工具使用能力**：能夠使用外部工具來擴展代理能力
3. **推理-行動循環**：結合推理和行動的方式有助於完成複雜任務
4. **自我反思**：能夠評估自己的行動結果並調整策略

### 缺點

1. **上下文限制**：難以處理超長上下文，如長篇小說生成
2. **多代理協作**：缺乏有效的多代理協作機制
3. **知識管理**：缺乏有效的知識管理和檢索機制
4. **連貫性保證**：難以保證長篇內容的連貫性和一致性
5. **抽象層次**：有些框架抽象層次過高，難以定制；有些則過於底層，使用複雜

## 改進方向

基於以上分析，我們的多智能體小說生成系統應該在以下方面進行改進：

1. **簡化核心框架**：保持核心框架的簡潔性，約1,000行代碼，但提供足夠的擴展性
2. **分層上下文管理**：實現分層的上下文管理，使用向量數據庫存儲和檢索知識
3. **專業化代理角色**：設計專業化的代理角色，如策劃、角色設計、章節撰寫等
4. **標準操作流程(SOP)**：為每個代理角色設計明確的SOP，確保協作效率
5. **自優化提示**：實現自監督的提示優化，提高生成質量
6. **思想原子分解**：將小說生成過程分解為思想原子，處理長上下文
7. **代碼化通信**：使用可執行代碼作為代理間通信的方式，提高明確性和可驗證性
8. **連貫性檢查機制**：設計專門的連貫性檢查機制，確保小說的連貫性和一致性

## 初步架構設想

基於以上研究，我們的多智能體小說生成系統可以採用以下架構：

1. **核心代理框架**：簡潔的核心框架，提供基本的代理功能和通信機制
2. **知識管理系統**：基於PostgreSQL向量數據庫的知識管理系統，支持分層概括和檢索
3. **多代理協作系統**：專業化的代理角色和明確的協作機制
4. **標準操作流程**：為每個代理角色設計的SOP，確保協作效率
5. **小說生成工作流**：從策劃到最終生成的完整工作流程
6. **連貫性保證機制**：確保小說連貫性和一致性的機制

這一架構將結合現有框架的優點，同時針對其缺點進行改進，實現高效的長篇小說生成。

# 智能小说创作助手

一个基于大型语言模型的智能小说创作工具，支持多种AI模型，能够自动生成完整的小说内容。

## 目录

- [功能特点](#功能特点)
- [安装说明](#安装说明)
- [使用方法](#使用方法)
- [输出说明](#输出说明)
- [项目结构](#项目结构)
- [自定义开发](#自定义开发)
- [注意事项](#注意事项)
- [许可证](#许可证)
- [贡献指南](#贡献指南)
- [更新日志](#更新日志)
- [联系方式](#联系方式)

## 功能特点

- 支持多种AI模型（浦语、智谱）
- 自动生成故事主题和核心思想
- 创建多维度的人物角色（包括主角、反派和配角）
- 生成详细的故事大纲
- 自动生成富有诗意的章节标题
- 分段生成完整的故事内容
- 自动保存JSON和TXT格式的输出

## 安装说明

### 步骤1: 克隆项目

```bash
git clone https://github.com/xiaoxiaoxiaotao/novel-ai-agent-Chinese.git
cd novel_ai_agent
```

### 步骤2: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤3: 配置API密钥

复制`.env.example`为`.env`并在其中填入你的API密钥：

#### 浦语模型配置

```plaintext
PUYU_API_KEY=your_puyu_api_key
PUYU_BASE_URL=your_puyu_base_url
```

#### 智谱AI配置

```plaintext
GLM_API_KEY=your_glm_api_key
GLM_BASE_URL=your_glm_base_url
```

## 使用方法

- **使用浦语模型创作故事**

  ```bash
  python story_creation_example.py --model puyu
  ```

- **使用智谱模型创作故事**

  ```bash
  python story_creation_example.py --model glm
  ```

## 输出说明

程序会在`output`目录下生成两个文件：

1. **JSON文件（`story_output_{model_type}_{timestamp}.json`）**：
   - 包含完整的故事元数据，如主题、角色设定、大纲等。

2. **TXT文件（`story_{model_type}_{timestamp}.txt`）**：
   - 包含可读的故事内容，包括章节标题和正文。

## 项目结构

```
novel_ai_agent/
├── src/
│ ├── __init__.py
│ ├── agent.py # AI代理核心逻辑
│ └── prompts.py # 提示词模板
├── output/ # 输出文件目录
├── .env # 环境配置文件
├── .gitignore # Git忽略文件
├── requirements.txt # 项目依赖
├── README.md # 项目说明
└── story_creation_example.py # 示例脚本
```

## 自定义开发

- **修改提示词**：编辑`src/prompts.py`中的提示词模板以调整故事风格、长度等参数。
- **调整输出格式**：修改`story_creation_example.py`中的输出处理逻辑来自定义输出文件的格式和内容。
- **添加新的模型支持**：在`src/agent.py`中扩展`NovelAIAgent`类并添加新的API调用方式。

## 注意事项

- 确保API密钥有效且有足够的配额。
- 生成的内容可能需要人工审核。
- 建议保留生成的JSON文件以便后续修改。
- 注意遵守API使用条款和版权规定。

## 许可证

本项目采用MIT License许可协议。详情参见[LICENSE](LICENSE)文件。

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 更新日志

### v1.0.0 (2025-01-01)

- 初始版本发布。
- 支持浦语和智谱AI模型。
- 实现基本的故事生成功能。

## 联系方式

如有问题或建议，请提交Issue或联系开发者。
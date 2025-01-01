import asyncio
import os
from dotenv import load_dotenv
from src.agent import NovelAIAgent, create_agent
import json
import logging
from datetime import datetime
import argparse

# 加载.env文件
load_dotenv()

logger = logging.getLogger(__name__)

# 模型配置
MODEL_CONFIGS = {
    "puyu": {
        "api_key": os.getenv("PUYU_API_KEY"),
        "base_url": os.getenv("PUYU_BASE_URL"),
        "model_type": "puyu",
        "model": "internlm2.5-latest"
    },
    "glm": {
        "api_key": os.getenv("GLM_API_KEY"),
        "base_url": os.getenv("GLM_BASE_URL"),
        "model_type": "glm",
        "model": "glm-4-flash"
    }
}

def load_story_prompt(genre: str) -> str:
    """加载并处理故事提示词"""
    try:
        with open("story_prompts.txt", "r", encoding="utf-8") as f:
            template = f.read()
            
        # 替换题材
        prompt = template.replace("{题材}", genre)
        
        # 构建完整的提示词
        formatted_prompt = f"""
请根据以下模板创作一个{genre}小说：

{prompt}

请确保故事情节合理，人物性格鲜明，冲突激烈，结构完整。
"""
        return formatted_prompt
        
    except Exception as e:
        logger.error(f"加载故事提示词时出错: {str(e)}")
        raise

async def create_sample_story(model_type: str = "puyu", genre: str = "科幻"):
    # 获取对应的模型配置
    config = MODEL_CONFIGS.get(model_type)
    if not config:
        raise ValueError(f"不支持的模型类型: {model_type}，请选择 'puyu' 或 'glm'")
    
    if not config["api_key"]:
        raise ValueError(f"请在.env文件中设置{model_type.upper()}_API_KEY")

    # 初始化AI代理
    agent = NovelAIAgent(
        api_key=config["api_key"],
        base_url=config.get("base_url"),
        model_type=model_type
    )

    # 加载故事提示词
    prompt = load_story_prompt(genre)

    # 创建故事
    story = await agent.create_story(prompt)
    
    # 创建输出目录结构
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_base = os.path.join("output", f"story_{model_type}_{timestamp}")
    os.makedirs(output_base, exist_ok=True)
    chapters_dir = os.path.join(output_base, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)

    # 准备元数据
    meta_info = {
        "model_type": model_type,
        "model_name": config["model"],
        "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": story.get("title", ""),
        "theme": story.get("themes", []),
        "setting": story.get("setting", ""),
        "characters": story.get("characters", ""),
        "tone": story.get("tone", ""),
        "outline": story.get("outline", ""),
        "chapters": story.get("synopses", [])
    }

    # 保存元数据
    with open(os.path.join(output_base, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)

    # 保存目录结构
    with open(os.path.join(output_base, "table_of_contents.md"), "w", encoding="utf-8") as f:
        f.write("# 故事目录\n\n")
        f.write(story["outline"].split("## 详细大纲")[0])  # 只保存目录部分

    # 保存每章内容
    if isinstance(story["content"], list):
        for i, chapter in enumerate(story["content"], 1):
            chapter_file = os.path.join(chapters_dir, f"chapter_{i:03d}.txt")
            with open(chapter_file, "w", encoding="utf-8") as f:
                f.write(chapter)
    else:
        logger.error("故事内容格式错误：不是章节列表")
        # 如果内容不是列表，将整个内容保存为单个文件
        with open(os.path.join(output_base, "full_story.txt"), "w", encoding="utf-8") as f:
            f.write(story["content"])

    logger.info(f"故事创作完成，输出目录：{output_base}")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='AI小说创作工具')
    parser.add_argument('--model', type=str, choices=['puyu', 'glm'], 
                       default='puyu', help='选择使用的模型 (puyu 或 glm)')
    parser.add_argument('--genre', type=str, default='科幻',
                       help='小说题材 (如：科幻、奇幻、悬疑等)')
    args = parser.parse_args()

    # 在Windows系统上运行异步代码
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 运行异步函数
    asyncio.run(create_sample_story(args.model, args.genre))

if __name__ == "__main__":
    main() 
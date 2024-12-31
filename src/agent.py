from typing import Dict, Optional, List
from openai import OpenAI
from zhipuai import ZhipuAI
import logging
from .prompts import (
    THEME_ANALYSIS_PROMPT,
    CHARACTER_DESIGN_PROMPT,
    STORY_OUTLINE_PROMPT,
    CONTENT_CREATION_SYSTEM_PROMPT,
    get_section_prompt,
    SECTION_TITLE_PROMPT
)
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NovelAIAgent:
    def __init__(self, api_key: str, base_url: Optional[str] = None, model_type: str = "puyu"):
        """初始化小说创作智能代理"""
        logger.info(f"初始化NovelAIAgent... (model_type: {model_type})")
        
        self.model_type = model_type
        if model_type == "puyu":
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = "internlm2.5-latest"
        else:  # glm
            self.client = ZhipuAI(api_key=api_key)
            self.model = "glm-4-flash"
            
        logger.info(f"API配置完成: model={self.model}")
        
        self.current_story = {
            "title": "",
            "outline": "",
            "characters": [],
            "themes": [],
            "content": ""
        }

    async def _call_api(self, messages: List[Dict]) -> str:
        """统一的API调用接口"""
        try:
            if self.model_type == "puyu":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return response.choices[0].message.content
            else:  # glm
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API调用出错: {str(e)}")
            raise
    
    async def create_story(self, prompt: str) -> Dict:
        """创建完整的故事"""
        try:
            logger.info("开始创建新故事...")
            logger.info(f"故事提示: {prompt[:100]}...")

            # 生成章节标题
            section_titles = await self._generate_section_titles()
            
            # 1. 分析主题和核心思想
            logger.info("Step 1/4: 分析故事主题...")
            themes_content = await self._call_api([
                {"role": "system", "content": THEME_ANALYSIS_PROMPT},
                {"role": "user", "content": prompt}
            ])
            themes = themes_content.split('\n')
            self.current_story["themes"] = themes
            logger.info(f"主题分析完成: 发现 {len(themes)} 个主题")
            
            # 2. 设计角色
            logger.info("Step 2/4: 设计故事角色...")
            characters = await self._call_api([
                {"role": "system", "content": CHARACTER_DESIGN_PROMPT},
                {"role": "user", "content": f"故事提示：{prompt}\n主题：{themes}"}
            ])
            self.current_story["characters"] = characters
            logger.info("角色设计完成")
            
            # 3. 创建故事大纲
            logger.info("Step 3/4: 创建故事大纲...")
            outline = await self._call_api([
                {"role": "system", "content": STORY_OUTLINE_PROMPT},
                {"role": "user", "content": f"故事提示：{prompt}\n主题：{themes}\n角色：{characters}"}
            ])
            self.current_story["outline"] = outline
            logger.info("故事大纲创建完成")
            
            # 4. 生成详细故事内容
            logger.info("Step 4/4: 生成详细故事内容...")
            story_content = await self._generate_story_content(outline, characters, section_titles)
            self.current_story["content"] = story_content
            logger.info("故事内容生成完成")
            
            logger.info("故事创作完成!")
            return self.current_story
            
        except Exception as e:
            logger.error(f"创作故事时出错: {str(e)}", exc_info=True)
            return {
                "themes": [],
                "characters": "",
                "outline": "",
                "content": ""
            }

    async def _generate_story_content(self, outline: str, characters: str, section_titles: Dict[str, str]) -> str:
        """生成详细的故事内容"""
        logger.info("开始生成详细故事内容...")
        story_sections = ["起因", "经过", "发展", "高潮", "结局"]
        story_content = []
        
        # 提取大纲中的各个部分
        logger.info("解析故事大纲...")
        outline_parts = {}
        current_part = None
        current_content = []
        
        for line in outline.split('\n'):
            if line.strip().startswith('【') and line.strip().endswith('】'):
                if current_part:
                    outline_parts[current_part] = '\n'.join(current_content).strip()
                current_part = line.strip('【】')
                current_content = []
            else:
                current_content.append(line)
        if current_part:
            outline_parts[current_part] = '\n'.join(current_content).strip()
        logger.info(f"大纲解析完成，共有 {len(outline_parts)} 个部分")

        # 为每个部分生成详细内容
        for i, section in enumerate(story_sections):
            logger.info(f"正在生成 {section} 部分 ({i+1}/{len(story_sections)})...")
            prev_section = story_sections[i-1] if i > 0 else None
            section_prompt = get_section_prompt(
                section=section,
                outline_part=outline_parts.get(section, '未提供'),
                characters=characters,
                prev_section=prev_section
            )
            
            try:
                section_content = await self._call_api([
                    {"role": "system", "content": CONTENT_CREATION_SYSTEM_PROMPT},
                    {"role": "user", "content": section_prompt}
                ])
                story_content.append(f"\n\n【{section}】\n\n{section_content}")
                logger.info(f"{section} 部分生成完成")
                
            except Exception as e:
                logger.error(f"生成 {section} 部分时出错: {str(e)}")
                story_content.append(f"\n\n【{section}】\n\n生成失败")
        
        logger.info("所有部分生成完成")
        return '\n'.join(story_content)

    async def _generate_section_titles(self) -> Dict[str, str]:
        """生成各部分的标题"""
        try:
            response = await self._call_api([
                {"role": "system", "content": SECTION_TITLE_PROMPT},
                {"role": "user", "content": "请为故事的五个部分生成标题"}
            ])
            titles = json.loads(response)
            logger.info(f"生成章节标题: {titles}")
            return titles
        except Exception as e:
            logger.error(f"生成章节标题时出错: {str(e)}")
            return {
                "起因": "《根基》",
                "经过": "《暗流》",
                "发展": "《激流》",
                "高潮": "《巨浪》",
                "结局": "《回归》"
            }

def create_agent(model_type: str, api_key: str, base_url: Optional[str] = None) -> NovelAIAgent:
    """创建AI代理"""
    return NovelAIAgent(api_key=api_key, base_url=base_url, model_type=model_type) 
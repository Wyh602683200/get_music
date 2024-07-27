import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://www.hhlqilongzhu.cn/api/dg_qqmusic.php?gm=泡沫&n=1" 
@plugins.register(name="get_music",
                  desc="搜歌曲",
                  version="1.0",
                  author="wyh",
                  desire_priority=100)

class get_music(Plugin):

    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【搜歌曲】或 【搜音乐】 获取歌曲链接"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        
        if self.content.startswith("搜歌曲") or self.content.startswith("搜音乐"):
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.get_music()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS


    def get_music(self):
        url = BASE_URL_DM
        params = {"gm":self.content.replace(" ", "")[3:]}            
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            # 主接口
            response = requests.get(url=url, params=params, headers=headers,timeout=10)
            if response.status_code == 200:
                # json_data = response.text                      
                # formatted_output = []
                # basic_info = (
                #     f"☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆\n"
                #     f"⌛ 歌曲: {json_data['name']}\n",
                #     f"⌛ 作者: {json_data['singer']}\n",
                #     f"⌛ 播放地址: {json_data['url']}\n"
                # )
                # basic_info = response.text      
                # formatted_output.append(basic_info)
                
                # return '\n'.join(['\n'.join(item) for item in formatted_output])
                return  response.text         
                
                
            else:
                logger.error(f"接口返回值异常:{json_data}")
                raise ValueError('not found')

        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("接口异常")
        return None




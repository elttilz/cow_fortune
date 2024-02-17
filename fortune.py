
# encoding:utf-8
import requests
import plugins
import json
from bridge.event import Handler, ContextType, Event, EventContext
from bridge.reply import TextReply,Reply, ReplyType
from plugins import *
from datetime import datetime
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="Fortune",
    desire_priority=-1,
    hidden=True,
    desc="A plugin for today's fortune",
    version="0.1",
    author="dajoe",
)

class Fortune(Plugin):
    def init(self):
        super().init()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content.strip()
        if '今日财运' in content:
            # Load the configuration values from the JSON file
            with open('config.json') as f:
                config = json.load(f)
            appkey = config['appkey']
            today = datetime.today().strftime('%Y-%m-%d')
            year, month, day = today.split('-')
            # Use the appkey in the request URL
            url = f"http://open.liupai.net/huangli/query?appkey={appkey}&year={year}&month={month}&day={day}"
            response = requests.get(url)
            data = response.json()
            if 'result' in data:
                result = data['result']
                reply_msg = f'''今日的财运如下：
                              年份: {result['year']}
                              月份: {result['month']}
                              日子: {result['day']}
                              财神方位: {result['caishen']} 
                              福神方位: {result['fushen']}
                              喜神方位: {result['xishen']}
                              今日宜做: {', '.join(result['yiji'])}
                              今日忌做: {', '.join(result['jiji'])}'''
                return reply_msg
# -*- coding:utf-8 -*-
import logging
from random import randint
import re
from typing import Callable
from wudao.api_request import getToken

"""
使用方法：
    1）使用者需要有大模型开放平台(open.bigmodel.cn)的账号。在登录了大模型开放平台后，在上方
       用户手册 -> 新手指南 -> 获取API keys 的页面中，点击 "管理 API Keys"的链接。
       通过 "添加新的 API Key" 的按钮，获取自己的API Key与Public Key，填入下面地两个相应
       变量中（API_KEY，PUBLIC_KEY）。
    2）使用者需要有python3的运行环境，目前本文件开发测试时使用的版本为3.10.4。
    3）使用时需要安装/升级wudao的package。安装/升级命令为：
       pip install --upgrade wudao
       对于国内用户，推荐使用清华的Mirror：
       pip3 install --upgrade wudao -i  https://pypi.tuna.tsinghua.edu.cn/simple/

    在完成以上操作后，就应该能够顺利执行本文件了。

程序介绍
    本程序的实现目标是提供一个对于chatglm api进行能力测试的基础实现。主要演示如何使用相关的API。
    目前版本，本程序支持多轮对话，但每次提问时仅支持单行输入。
    在正常的输入之外，额外提供以下两个命令：
        history     该命令会将当前会话带的所有历史信息全部打出。
        clear       清空多轮对话的历史信息
    如果需要退出本程序，请直接 Ctrl+C。
    
"""

def randomTaskCode():
    return "%019d" % randint(0, 10**19)

MODEL_REQUEST_URL = "https://maas.aminer.cn/api/paas/model/v1/open/engines/sse/chatGLM/chatGLM"

# 接口API KEY
API_KEY = "50ed7642af964563860c6f224b013062"
# 公钥
PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAK8KZcpPMnHqoCN6pXtDjrxeiIa6KHjmFEx+nrF/Zks5baspFh9XpTdmyIrRh306YMYWipcKHnZOMweVzFVzos0CAwEAAQ=="

# 能力类型
ability_type = "chatGLM"
# 引擎类型
engine_type = "chatGLM"

token_result = getToken(API_KEY, PUBLIC_KEY)

_FIELD_SEPARATOR = ":"

def punctuation_converse_auto(msg):
    punkts = [
        [",", "，"],
        ["!", "！"],
        [":", "："],
        [";", "；"],
        ["\?", "？"],
    ]
    for item in punkts:
        msg = re.sub(r"([\u4e00-\u9fff])%s" % item[0], r"\1%s" % item[1], msg)
        msg = re.sub(r"%s([\u4e00-\u9fff])" % item[0], r"%s\1" % item[1], msg)
    return msg

def prepare_print_diff(nextStr: Callable[[any], str], printError: Callable[[], None]):
    previous = ""
    def print_diff(input):
        nonlocal previous
        str = nextStr(input)
        if (not str.startswith(previous)):
            last_line_index = str.rfind("\n") + 1
            if (previous.startswith(str[0: last_line_index])):
                print("\r%s" % str[last_line_index:], end="", flush=True)
            else:
                print()
                print(1, "[[previous][%s]]" % previous)
                printError(input)
        else:
            print(str[len(previous):], end="", flush=True)
        previous = str

    return print_diff

def print_history(history):
    is_request = True
    for history_item in history:
        print("Request:" if is_request else "Response:")
        print("\t", history_item)
        is_request = not is_request

class SSEClient(object):
    """Implementation of a SSE client.
    See http://www.w3.org/TR/2009/WD-eventsource-20091029/ for the
    specification.
    """

    def __init__(self, event_source, char_enc="utf-8"):
        """Initialize the SSE client over an existing, ready to consume
        event source.
        The event source is expected to be a binary stream and have a close()
        method. That would usually be something that implements
        io.BinaryIOBase, like an httplib or urllib3 HTTPResponse object.
        """
        self._logger = logging.getLogger(self.__class__.__module__)
        self._logger.debug("Initialized SSE client from event source %s",
                           event_source)
        self._event_source = event_source
        self._char_enc = char_enc

    def _read(self):
        """Read the incoming event source stream and yield event chunks.
        Unfortunately it is possible for some servers to decide to break an
        event into multiple HTTP chunks in the response. It is thus necessary
        to correctly stitch together consecutive response chunks and find the
        SSE delimiter (empty new line) to yield full, correct event chunks."""
        data = b""
        for chunk in self._event_source:
            for line in chunk.splitlines(True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    def events(self):
        for chunk in self._read():
            event = Event()
            # Split before decoding so splitlines() only uses \r and \n
            for line in chunk.splitlines():
                # Decode the line.
                line = line.decode(self._char_enc)

                # Lines starting with a separator are comments and are to be
                # ignored.
                if not line.strip() or line.startswith(_FIELD_SEPARATOR):
                    continue

                data = line.split(_FIELD_SEPARATOR, 1)
                field = data[0]

                # Ignore unknown fields.
                if field not in event.__dict__:
                    self._logger.debug(
                        "Saw invalid field %s while parsing "
                        "Server Side Event", field)
                    continue

                if len(data) > 1:
                    # From the spec:
                    # "If value starts with a single U+0020 SPACE character,
                    # remove it from value."
                    if data[1].startswith(" "):
                        value = data[1][1:]
                    else:
                        value = data[1]
                else:
                    # If no value is present after the separator,
                    # assume an empty value.
                    value = ""

                # The data field may come over multiple lines and their values
                # are concatenated with each other.
                if field == "data":
                    event.__dict__[field] += value + "\n"
                else:
                    event.__dict__[field] = value

            # Events with no data are not dispatched.
            if not event.data:
                continue

            # If the data field ends with a newline, remove it.
            if event.data.endswith("\n"):
                event.data = event.data[0:-1]

            # Empty event names default to 'message'
            event.event = event.event or "message"

            # Dispatch the event
            self._logger.debug("Dispatching %s...", event)
            yield event

    def close(self):
        """Manually close the event source stream."""
        self._event_source.close()


class Event(object):
    """Representation of an event from the event stream."""

    def __init__(self, id=None, event="message", data="", retry=None, meta={}):
        self.id = id
        self.event = event
        self.data = data
        self.retry = retry
        self.meta = meta

    def __str__(self):
        s = "{0} event".format(self.event)
        if self.id:
            s += " #{0}".format(self.id)
        if self.data:
            s += ", {0} byte{1}".format(len(self.data),
                                        "s" if len(self.data) else "")
        else:
            s += ", no data"
        if self.retry:
            s += ", retry in {0}ms".format(self.retry)
        return


if __name__ == "__main__":
    import requests
    import pprint
    if token_result and token_result["code"] == 200:
        token = token_result["data"]
        headers = {"Authorization": token}

        history = []
        print()
        print("'clear' to clear history and 'history' to show history. Ctrl-C to exit")
        while (True):
            print("Your Input:")
            prompt = input()
            print()
            
            if prompt == "clear":
                history = []
                print("History Cleared.")
                continue
            elif prompt == "history":
                # print("\n".join(history))
                print_history(history)
                print()
                continue

            json = {
                "top_p": 0.7,
                "temperature": 0.7,
                "risk": 0.15,
                "prompt": prompt,
                "requestTaskNo": randomTaskCode(),
                "history": history,
            }

            response = requests.post(
                MODEL_REQUEST_URL,
                headers=headers,
                json=json,
                stream=True,
            )
            client = SSEClient(response)
            print_diff = prepare_print_diff(lambda e: e.data, lambda e: pprint.pprint(e.__dict__))
            print('Response: ')
            for event in client.events():
                if (event.data):
                    event.data = punctuation_converse_auto(event.data)
                if (event.event == "add"):
                    print_diff(event)
                elif (event.event == "finish" or event.event == "interrupted"):
                    print_diff(event)
                    print()
                    history.extend([prompt, event.data])
                    break
                else:
                    pprint.pprint(event)
            print()
    else:
        print("获取token失败，请检查 API_KEY 和 PUBLIC_KEY")



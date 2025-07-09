import click, json, os


__file__ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rename_tool.py")
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mrliu_tools.json"), "r") as f:
        js = json.load(f)
        lang = js["language"]
except Exception as e:
    click.secho(f"Error loading configuration: {e}", fg="red")
    lang = "en"  # Default to English if there's an error


icon_command = {
    "colors" :[
        'red', 'bright_red', 'yellow', 'bright_yellow', 'green',
        'bright_green', 'cyan', 'bright_cyan', 'blue', 'bright_blue',
        'magenta', 'bright_magenta'
    ],
    "text_lines" :[
        " __  __        _      _            ______            __    ",
        "|  \/  | _ __ | |    (_) _   _    /_  __/___  ____  / /____",
        "| |\/| || '__|| |    | || | | |    / / / __ \/ __ \/ / ___/",
        "| |  | || |   | |___ | || |_| |   / / / /_/ / /_/ / (__  )",
        "|_|  |_||_|   |_____||_| \__,_|  /_/  \____/\____/_/____/ "
    ]
}


help_text = {
    "zh": {
        "rename": {
            "description": "批量重命名文件",
            "options": {
                "-p": "需要批量重命名的文件所在路径",
                "-pt": "匹配文件的正则表达式",
                "-t": "批量重命名的格式",
                "-wd": "同时重命名目录",
                "-od": "仅重命名目录(不重命名文件)",
                "-r": "恢复上一次的重命名操作",
                "--more-help": "获取更多帮助"
            }
        },
        "audio_send": {
            "description": "将本机声音通过网络实时发送到另一台电脑",
            "options": {
                "receiver_ip": "接收方的IP地址",
                "--port": "目标端口",
                "--rate": "采样率",
                "--channels": "声道数",
                "--chunk": "每帧采样点数"
            }
        },
        "audio_recv": {
            "description": "接收网络音频并播放(适用于已连接蓝牙音箱的电脑)",
            "options": {
                "--port": "监听端口",
                "--rate": "采样率",
                "--channels": "声道数",
                "--chunk": "每帧采样点数"
            }
        },
        "set_language": {
            "description": "设置命令行工具的语言(en/zh)",
            "options": {
                "lang": "语言(en/zh)"
            }
        }
    },
    "en": {
        "rename": {
            "description": "Batch rename files",
            "options": {
                "-p": "The path where batch renaming is needed.",
                "-pt": "Regular expressions to match files.",
                "-t": "Batch rename format.",
                "-wd": "Rename the directories simultaneously.",
                "-od": "Only rename the directories (do not rename files).",
                "-r": "Restore the last rename operation.",
                "--more-help": "Get more help."
            }
        },
        "audio_send": {
            "description": "Stream local audio to another computer over the network",
            "options": {
                "receiver_ip": "IP address of the receiver",
                "--port": "Target port",
                "--rate": "Sample rate",
                "--channels": "Number of channels",
                "--chunk": "Number of samples per frame"
            }
        },
        "audio_recv": {
            "description": "Receive and play network audio (suitable for computers connected to Bluetooth speakers)",
            "options": {
                "--port": "Listening port",
                "--rate": "Sample rate",
                "--channels": "Number of channels",
                "--chunk": "Number of samples per frame"
            }
        },
        "set_language": {
            "description": "Set the language of the command line tool (en/zh)",
            "options": {
                "lang": "Language (en/zh)"
            }
        }
    }
}


more_help = {
    "zh": "此工具使用re库实现,下面是一些修饰符\n"
        "1.?time=<FORMAT>; - 指定日期(时间)格式\n"
        "2.?count; - 序号,每次递增\n"
        "3.?text=<TEXT>; - 插入文本(也可以直接插入)\n"
        "4.?ext; - 只取后缀名\n"
        "5.?name; - 只取文件名(不包括地址和后缀名)\n"
        "6.?md5; - 获取文件的md5值\n"
        "7.?parent; - 获取父文件名\n"
        "8.?rand=<N>; - 生成N位随机字符串\n"
        "9.?user; - 当前操作系统用户名\n"
        "10.?upper;/?lower; - 文件名转大写或小写",
    "en": "This tool is implemented using the re library. Below are some modifiers:\n"
        "1.?time=<FORMAT>; - Specify the date (time) format\n"
        "2.?count; - Sequence number, increments each time\n"
        "3.?text=<TEXT>; - Insert text (can also be inserted directly)\n"
        "4.?ext; - Get only the file extension\n"
        "5.?name; - Get only the filename (excluding path and extension)\n"
        "6.?md5; - Get the MD5 value of the file\n"
        "7.?parent; - Get the parent directory name\n"
        "8.?rand=<N>; - Generate an N-digit random string\n"
        "9.?user; - Current operating system username\n"
        "10.?upper;/?lower; - Convert filename to uppercase/lowercase",
}


def help_(command, lang="en"):
    if lang == "zh" :
        return help_text["zh"][command]
    else:
        return help_text["en"][command]

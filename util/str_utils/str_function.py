# 计算一个字符串的单词数量(评论中的链接不算在内)
def wordCount(str) -> int:
    """
        计算某个字符串中单词数量，输入参数为字符串
        “Thanks! Should I create issue for this PR?\n”
        输出整型数字 8
        评论中的链接计算为一个单词
    """
    num = 0
    if str is None or str == '' or str == ' ' or len(str) == 0:
        num = 0
    else:
        num = len(str.strip().split(' '))
    return num



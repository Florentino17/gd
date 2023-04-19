# 获取本地文件中的access_tocken相关值
def get_token(num=0):
    file = open('F:\\tmp\\access_token.txt', 'r')
    list = file.readlines()
    lines = len(list)
    #str = file.readline()
    print("【util/str_utils/access_token.py】number of access_token lines = ",lines)
    str = list[num % lines] #多个token可以循环使用，并行工作
    file.close()
    print("【util/str_utils/access_token.py】access_token==",str)
    return str


# get_token()

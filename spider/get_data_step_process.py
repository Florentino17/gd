from spider_pr_file import get_pr_file_info
from spider_pr_repo import get_repo_info
from spider_pr_self import get_pr_self_info
from spider_pr_user import get_pr_user_info
import sys
import os
sys.path.append(os.getcwd()) 
from util.access_token import get_token
####


if __name__ == '__main__':


    # print("testeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    # 此部分可修改，用于控制进程
    # index = 3228         #i 开始的序号
    index=0 
    max_pr_num = 45094  #7784 59282  #i 最大pr数量  github找，第一个pr的id  max(open,close)
    # "openzipkin/zipkin"

    # owner_name = "activemerchant"  # "spring-projects"  # "symfony"#"rails"#"angular" #"tensorflow"   #i拥有者姓名
    # repo_name = "active_merchant"  # "spring-framework"  # "spring-boot" #"symfony"#"rails"#"angular.js"#"tensorflow"   #i repo名字（仓库？）
    owner_name = "moby"  # "spring-projects"  # "symfony"#"rails"#"angular" #"tensorflow"   #i拥有者姓名
    repo_name = "moby"  # "spring-framework"  # "spring-boot" #"symfony"#"rails"#"angular.js"#"tensorflow"   #i repo名字（仓库？）
    #zendframework  tensorflow   Ipython   Katello  opencv  terraform
    # pass
    # print("test")
    access_token = get_token()    #i 获取token不知道什么
    headers = {
        'Authorization': 'token ' + access_token    #i 授权：token +access_token（？）
    }


    # index=0
    # get_repo_info(index, owner_name, repo_name, headers)   #i 存储仓库信息
    # print(owner_name+": repo "+repo_name+"—===============================仓库信息存储完毕=======================")
    # print(owner_name+": repo "+repo_name+"—===============================仓库信息存储完毕=======================")
    # print(owner_name+": repo "+repo_name+"—===============================仓库信息存储完毕=======================")
    # print("index=================",index)


    # index=44600
    # num_sum=0
    # last_index=index
    # newindex=index
    # while (1):
    #     last_index=newindex
    #     newindex=get_pr_self_info(newindex, max_pr_num, owner_name, repo_name, headers)  #i 存储pr_self信息
    #     print(owner_name+": pr_self "+repo_name+"—===============================pr_self信息存储完毕=======================")
    #     print(owner_name+": pr_self "+repo_name+"—===============================pr_self信息存储完毕=======================")
    #     print(owner_name+": pr_self "+repo_name+"—===============================pr_self信息存储完毕=======================")
    #     print("newindex=================",newindex) 
    #     print("newindex=================",newindex) 
    #     print("newindex=================",newindex) 
    #     print("newindex=================",newindex) 
    #     if last_index==newindex:
    #         if num_sum<=1:
    #             num_sum+=1
    #         else:
    #             newindex+=1
    #             num_sum=0
    #     if newindex>max_pr_num:
    #         break


    # index=7339
    # get_pr_file_info(index, repo_name, headers)         #i 存储pr_file信息
    # print(owner_name+": pr_file "+repo_name+"—===============================pr_file信息存储完毕=======================")
    # print(owner_name+": pr_file "+repo_name+"—===============================pr_file信息存储完毕=======================")
    # print(owner_name+": pr_file "+repo_name+"—===============================pr_file信息存储完毕=======================")
    # print("index=================",index)
    # # alter table pr_file auto_increment = 8555; 下一个应该的id值

    # index=0
    # get_pr_user_info(index, repo_name, headers)             #i 存储pr_user信息
    # print(owner_name+": pr_user "+repo_name+"—===============================pr_user信息存储完毕=======================")
    # print(owner_name+": pr_user "+repo_name+"—===============================pr_user信息存储完毕=======================")
    # print(owner_name+": pr_user "+repo_name+"—===============================pr_user信息存储完毕=======================")   
    # print("index=================",index)




    import tkinter.messagebox as msgbox
    msgbox.showinfo("结束")

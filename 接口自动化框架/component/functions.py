import requests
import json
import hashlib
import os
import pickle
import re

success_case_num = 0
fail_case_num = 0
total_case_num = 0

flag = True

var_dict={}#存储接口返回的部分数据


def md5(s):
    # 动态计算md5的函数
    m5 = hashlib.md5()
    m5.update(s.encode("utf-8"))
    pwd = m5.hexdigest()
    return pwd

def get_unique_num():
    if not os.path.exists("number.txt"):
        num =1100
        fp = open("number.txt","wb")
        pickle.dump(num+1,fp)
        fp.close()
        return num
    else:
        fp = open("number.txt", "rb")
        num= pickle.load(fp)
        fp.close()
        fp = open("number.txt", "wb")
        pickle.dump(num+1,fp)
        fp.close()
        return num

def print_report():
    global  success_case_num,fail_case_num
    print("*"*30)
    print("""    测试用例执行结果统计：
    成功执行的用例数：%s
    失败执行的用例数：%s
    执行的用例总数：%s""" % (success_case_num, fail_case_num, success_case_num + fail_case_num))
    print("*"*30)

def request(request_url,request_method,request_data):
    try:
        if "post" in str(request_method).lower():
            req = requests.post(url=request_url, data=json.dumps(request_data))
        elif "put" in str(request_method).lower():
            req = requests.put(url=request_url, data=json.dumps(request_data))
        elif "get" in str(request_method).lower():
            if request_data:
                request_url=request_url+str(request_data)
            req = requests.get(url=request_url)
    except Exception as e:
        print("请求方法：%s,请求url:%s,请求数据：%s 发出请求出现异常:%e" %(request_method,request_url,request_data,e))
        return ""
    return req.text

def assert_result(interface_info,req,*assert_word):
    global success_case_num,fail_case_num,flag
    flag=True
    exception_info = ""
    for word in assert_word:
        try:
            assert re.search(word, req),"断言词：%s,响应结果：%s" %(word,req)
        except AssertionError as e:
            print("断言%s接口时候失败，断言信息：%s" %(interface_info,e))
            flag = False
            exception_info = "断言%s接口时候失败，断言信息：%s\n" %(interface_info,e)
        except Exception as e:
            print("断言%s接口时候出现非断言异常，异常信息：%s\n" %(interface_info,e))
            exception_info ="断言%s接口时候出现非断言异常，异常信息：%s\n" %(interface_info,e)

    if flag:
        add_success_case_num()
    else:
        add_fail_case_num()
    return flag,exception_info


def get_user_name(prefix=None):
    global var_dict
    if prefix:
        user_name = prefix + str(get_unique_num())
    else:
        user_name = "wulaoshiyx" + str(get_unique_num())
    var_dict["user_name"]= user_name
    return user_name

def handle_var(data):#把数据行中的变量部分，进行替换
    count=0
    try:
        while re.search(r"\$\{.*?\}",data):
            var_name = re.search(r"\$\{(.*?)\}",data).group(1)
            if  "md5" in re.search(r"\$\{.*?\}",data).group():
                md5_exp = re.search(r"\$\{.*(md5\(.*?\))\}",data).group(1)
                md5_value = eval(md5_exp)
                data = re.sub(r"\$\{.*(md5\(.*?\))\}", md5_value, data, 1)
            elif "unique_user_name" in var_name:
                value = get_user_name()
                data = re.sub(r"\$\{.*?\}",value,data,1)
            elif var_name in var_dict.keys():
                data = re.sub(r"\$\{.*?\}", var_dict[var_name], data, 1)
            count+=1
            if count==100:
                break
    except Exception as e:
        print("处理数据 %s 中的变量时出现了异常：%s" %(data,e))
        return None
    return data

def extract_var(data,req):
    global var_dict
    extract_var_data = data
    if extract_var_data.strip() :
        extract_var_name = extract_var_data.split("##")[0].strip()#拿到了要提取的变量名称
        extract_var_exp = extract_var_data.split("##")[1].strip()#拿到了提取变量名称的表达式
        if re.search(extract_var_exp,req):
            value_arr = re.findall(extract_var_exp,req)
            if len(value_arr)==1:
                var_dict[extract_var_name]=re.findall(extract_var_exp,req)[0]
            else:
                for i in range(len(value_arr)):
                    if i==0:
                        var_dict[extract_var_name] =value_arr[i]
                    else:
                        var_dict[extract_var_name+str(i)] = value_arr[i]

def print_test_process_info(data,url,request_method,assert_words,request_data,req,test_result,exception_info,var_dict):
    print("*"*50)
    print("测试数据行：",str(data))
    print("请求的url:",url)
    print("请求的方法：",request_method)
    print("断言词：",assert_words)
    print("请求的数据：",request_data)
    print("接口的响应结果：",req)
    print("测试时发生的异常信息：",exception_info)
    if test_result==True:
        print("用例的执行结果：","成功")
    else:
        print("用例的执行结果：", "失败")
    print("提取后的变量字典：",var_dict)

def add_success_case_num():
    global success_case_num
    success_case_num+=1

def add_fail_case_num():
    global fail_case_num
    fail_case_num+=1
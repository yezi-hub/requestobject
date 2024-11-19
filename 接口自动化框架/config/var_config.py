import os
"""管理各种工程中使用的各种文件路径以及excel中的某些列号"""

# 获得当前文件所在的目录
proj_path = os.path.dirname(os.path.dirname(__file__))

#数据文件的路径
test_data_file_path = os.path.join(proj_path,"test_data","接口测试用例.xlsx")
test_data_dir_path = os.path.join(proj_path,"test_data")

#报告目录路径
report_dir_path = os.path.join(proj_path,"report")
#报告文件html模板文件路径
template_file_path = os.path.join(proj_path,"util","test.html")

ip = "124.223.167.147"
port = "8080"

register = "http://%s:%s/register/"%(ip,port)
login = "http://%s:%s/login/"%(ip,port)
create = "http://%s:%s/create/"%(ip,port)
get_user_blogs = "http://%s:%s/getBlogsOfUser/" %(ip,port)
udpate = "http://%s:%s/update/" %(ip,port)
get_blog_content= "http://%s:%s/getBlogContent/" %(ip,port)
delete = "http://%s:%s/delete/" %(ip,port)

no_col_no = 0
interface_name_col_no = 1
request_method_col_no = 2
request_data_with_vars_col_no = 3
request_data_col_no = 4
response_col_no = 5
assert_words_col_no = 6
extract_var_exp_col_no = 7
execute_flag_col_no = 8
test_time__col_no = 9
interface_test_elapse_time_col_no = 10
test_result_col_no = 11
exception_info_col_no = 12

test_case_sheet_name_col_no = 2
test_case_execute_flag_col_no = 3
test_case_test_result_col_no =4
test_case_execute_time_col_no = 5
test_case_exception_info_col_no =6

if __name__=="__main__":
    print(proj_path)
    print(test_data_file_path)
    print(report_dir_path)
    print(template_file_path)
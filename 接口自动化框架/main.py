import multiprocessing
import os.path

from config.var_config import *
from component.functions import *
from util.excel_util import *
from util.generate_report import *
from util.time_util import *
from util.data_handle import *
import component.functions



def get_test_cases(wb,sheet_name,valid_flag_col_no):
    wb.set_sheet(sheet_name)
    test_cases = wb.get_all_rows_values()
    test_cases=remove_none_from_arr(test_cases)
    valid_test_cases = [test_cases[0]]
    #读取有效的测试用例行
    for test_case in test_cases[1:]:
        if "y" in str(test_case[valid_flag_col_no]).lower():
            valid_test_cases.append(test_case)

    return valid_test_cases

def execute_test_case_by_sheet(wb,sheet_name,report_file_path):
    test_cases = get_test_cases(wb,sheet_name,8)
    flag = "成功"
    print(test_cases)
    success_case_nums = 0
    fail_case_nums = 0
    for i in range(1,len(test_cases)):
        test_case = test_cases[i]
        test_process_data = []
        id = i
        test_case_test_result = "成功"
        url = ""
        request_method = ""
        request_data_with_var = ""
        request_data = ""
        assert_words = ""
        req = ""
        execute_time = ""
        test_elapse_time = ""
        exception_info = ""
        try:
            url = eval(test_case[interface_name_col_no])
            request_method = test_case[request_method_col_no]
            request_data_with_var = test_case[request_data_with_vars_col_no]
            assert_words = test_case[assert_words_col_no].split("##")
        except Exception as e:
            print("从%s中提取测试数据的过程出现异常，信息： %s" % (test_case, e))
            add_fail_case_num()
            test_case_test_result ="失败"
            continue
        lock = multiprocessing.Lock()
        with lock:
            try:
                request_data = handle_var(request_data_with_var)
                if not request_data:
                    add_fail_case_num()
                    continue
                execute_time = get_chinese_time()
                start_time = time.time()
                req = request(url, request_method, eval(request_data))
                end_time = time.time()
                test_elapse_time = str(round(end_time - start_time, 3) * 1000) + "毫秒"
                test_result, exception_info = assert_result(test_case[interface_name_col_no], req, *assert_words)
                extract_var(test_case[extract_var_exp_col_no], req)
            except Exception as e:
                traceback.print_exc()
                test_result = False
                add_fail_case_num()
                exception_info += traceback.format_exc()
                test_case_test_result = "失败"

        try:
            print_test_process_info(test_case, url, request_method, assert_words, request_data, req,test_result,exception_info, var_dict)
        except Exception as e:
            traceback.print_exc()
            print("打印测试结果的时候出现异常：%s" % e)
            exception_info += traceback.format_exc()


        if test_result:
            test_result = "成功"
            success_case_nums += 1
        else:
            test_result = "失败"
            flag = "失败"
            fail_case_nums +=1

        test_case[interface_name_col_no]=url
        test_case[request_data_col_no]=request_data
        test_case[response_col_no]=req
        test_case[test_result_col_no]=test_result
        test_case[test_time__col_no]=execute_time
        test_case[interface_test_elapse_time_col_no]=test_elapse_time
        test_case[exception_info_col_no]=exception_info
    wb.set_sheet("测试结果")
    wb.write_lines(test_cases,header_color="green")
    wb.save()
    gen_html_report(report_file_path,test_cases)
    return flag,exception_info,success_case_nums,fail_case_nums


def execute_test_case_by_file(test_data_file_path,report_file_path):
    wb = Excel(test_data_file_path)
    test_cases = get_test_cases(wb,"测试用例",test_case_execute_flag_col_no)
    success_case_count = 0
    fail_case_count = 0
    for i in range(1,len(test_cases)):
        test_case_sheet_name = test_cases[i][test_case_sheet_name_col_no]
        if test_case_sheet_name:
            test_cases[i][test_case_execute_time_col_no]=get_chinese_time()
            test_result,exception_info,success_num,fail_num=execute_test_case_by_sheet(wb, test_case_sheet_name,report_file_path)
            success_case_count += success_num
            fail_case_count += fail_num
            test_cases[i][test_case_test_result_col_no] = test_result
            test_cases[i][test_case_exception_info_col_no] = exception_info
            wb.set_sheet("测试结果")
            wb.write_a_line(test_cases[0],fill="green")
            wb.write_a_line(test_cases[i])
            wb.save()
            gen_html_report(report_file_path, [test_cases[0],test_cases[i]])
        else:
            continue
    return success_case_count,fail_case_count


def execute_test_case_by_dir(test_data_dir,report_file_path):
    if not os.path.exists(test_data_dir):
        print("测试目录 %s 不存在" %test_data_dir)
    print("2222222222222222",test_data_dir)
    test_data_files = []
    for root,dirs,files in os.walk(test_data_dir):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root,file)
                test_data_files.append(file_path)

    success_cases = 0
    fail_cases = 0
    for test_data_file in test_data_files:
        print("---",test_data_file)
        success_count,fail_count=execute_test_case_by_file(test_data_file, report_file_path)
        success_cases += success_count
        fail_cases += fail_count
    return success_cases,fail_cases


def task(queue,report_file_path):
    s = 0
    f = 0
    while not queue.empty():
        test_data_file_path = queue.get()
        print("************",test_data_file_path)
        try:
            s_n,f_n = execute_test_case_by_dir(test_data_file_path,report_file_path)
            s += s_n
            f += f_n
        except:
            print(traceback.print_exc())
            print(traceback.format_exc())
            print("异常")

    data = f"用例总数:{s + f} </br>" + f"成功用例总数：{s}</br>" + f"失败用例总数：{f}</br>"
    write_html_summary_line(report_file_path, data)


def concurrent_execute_test_case_by_dir(test_data_dir,report_file_path):
    if not os.path.isdir(test_data_dir):
        print("测试用例的目录 %s 不存在，无法并发执行！" % test_data_dir)
        return

    test_data_dir_queue = multiprocessing.Queue()
    for i in os.listdir(test_data_dir):
        if os.path.isdir(os.path.join(test_data_dir,i)):
            dir_path = os.path.join(test_data_dir,i)
            print("----------------",dir_path)
            test_data_dir_queue.put(dir_path)

    processes = []
    for i in range(2):
        #进程
        process = multiprocessing.Process(target=task,args=(test_data_dir_queue,report_file_path))
        processes.append(process)
        process.start()
        time.sleep(3)

    for process in processes:
        process.join()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(read_test_cases(test_data_file_path,"测试用例",3))
    #print(read_test_cases(test_data_file_path,"博客系统接口用例",7))
    report_file_path = get_report_file_path()
    # wb = Excel(test_data_file_path)
    # execute_test_case_by_dir(test_data_dir_path,report_file_path)
    concurrent_execute_test_case_by_dir(test_data_dir_path,report_file_path)



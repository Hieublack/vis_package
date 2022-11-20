import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean

from vis_package.method_test import Method

class Power(Method):
    def __init__(self) -> None:
        Method.__init__(self)
        self._alpha_power = ''
        self._index_file_power = 0
        self._index_file_qk_power = 0
        self._index_ht_power = 0
        self._index_qk_power = 0
        self._result_power = []
        self._index_power = []
        self._index_vetcan_power = []
        self._element_power = ""
        self._last_op_power = ""
        self._n = 1

    def _size_Element_power(self, listSizeEle, sizeEle, total_size):
        '''
        listSizeEle: danh sách chứa các kiểu phân tách công thức (cứ 2 giá trị kề nhau là 1 cấu trúc (số biến trên tử & số biến dưới mẫu) cho công thức con trong công thức, )
        sizeEle: danh sách chứa số biến của các thành phần con

        return : listSizeEle
        '''
        if sum(sizeEle) == total_size:
            if len(sizeEle) % 2 == 1:
                sizeEle.append(0)
                listSizeEle.append(sizeEle.copy())
                sizeEle.pop()
            else:
                listSizeEle.append(sizeEle.copy())
        else:
            if len(sizeEle) == 0:
                for i in range(1, total_size - sum(sizeEle)+1):
                    sizeEle.append(i)
                    self._size_Element_power(listSizeEle, sizeEle, total_size)
                    sizeEle.pop()
            else:
                if len(sizeEle) % 2 == 1:
                    for i in range(total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._size_Element_power(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
                else:
                    for i in range(1, total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._size_Element_power(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
        return listSizeEle

    def _process_result_size_Element_power(self, listSizeEle):
        '''
        listSizeEle: danh sách chứa các kiểu phân tách công thức (cứ 2 giá trị kề nhau là 1 cấu trúc (số biến trên tử & số biến dưới mẫu) cho công thức con trong công thức)
        list_new_size_element: danh sách chứa các kiểu phân tách công thức mà phần tử ứng với số biến dưới mẫu = 0
        '''
        list_new_size_element = []
        for item in listSizeEle:
            check = True
            for i in range(1, len(item), 2):
                if item[i] > 0:
                    check = False
            if check == True:
                list_new_size_element.append(item)
        return list_new_size_element

    def _get_same_even_odd_power(self, list_dict_Ele_structure):
        '''
        list_dict_Ele_structure: danh sách chứa các kiểu phân tách công thức mà phần tử ứng với số biến dưới mẫu = 0
        new_size_element: danh sách chứa các kiểu phân tách mà số biến ở tử số là cùng chẵn hoặc cùng lẻ
        '''
        new_size_element = []
        for item in list_dict_Ele_structure:
            mod_arr = np.mod(np.array(item), 2)
            if np.sum(mod_arr) == 0:
                new_size_element.append(item)
            elif np.sum(mod_arr) == len(mod_arr)/2:
                new_size_element.append(item)
        return new_size_element

    def _get_power(self, item_full):
        '''
        item_full: kiểu phân tách công thức

        return: các bậc của công thức con có thể để các công thức con trong công thức cùng bậc
        '''
        item = [item_full[i] for i in range(0, len(item_full), 2)]
        bac = np.min(item)
        list_bac = []
        list_bac_possible = [bac-2*x for x in range(round(bac/2)+1)]
        for bac in list_bac_possible:
            if bac > 0:
                list_bac.append(bac)
        return list_bac

    def _preProcessListSize_power(self, new_size_element):
        '''
        phân tách lại cấu trúc công thức để các công thức con có cùng bậc
        new_size_element: danh sách chứa các kiểu phân tách mà số biến ở tử số là cùng chẵn hoặc cùng lẻ

        return: danh sách các cấu trúc công thức mới
        '''
        list_all_bac = []
        for item in new_size_element:
            list_all_bac.append(self._get_power(item))
        list_all_size_element = []
        for id in range(len(list_all_bac)):
            size_element = new_size_element[id]
            list_bac = list_all_bac[id]
            for bac in list_bac:
                temp_size_element = size_element.copy()
                check = True
                for i in range(0, len(size_element), 2):
                    if temp_size_element[i] > bac:
                        temp_size_element[i+1] = int((temp_size_element[i] - bac)/2)
                        temp_size_element[i] = int((temp_size_element[i] + bac)/2)
                list_all_size_element.append(temp_size_element)
                temp_size_element = []
        return list_all_size_element

    def _processListSize_power(self, listSizeEle):
        '''
        listSizeEle: danh sách chứa các kiểu phân tách công thức

        result: list các dict mà mỗi dict là một cấu trúc công thức, mỗi thành phần trong dict là một cấu trúc 
                của công thức con (key) cùng số lượng (value) của kiểu công thức con đó trong công thức

        return : result 
        '''

        result = []
        for i in range(len(listSizeEle)):
            listSizeEle[i] = [(listSizeEle[i][j], listSizeEle[i][j+1])
                            for j in range(0, len(listSizeEle[i]), 2)]
            listSizeEle[i].sort(key=lambda x: x[0])
            listSizeEle[i].sort(key=lambda x: x[0]+x[1])
        dict_list = {}
        for i in range(len(listSizeEle)):
            try:
                k = dict_list[str(listSizeEle[i])]
            except:
                dict_list[str(listSizeEle[i])] = 1
                result.append(listSizeEle[i])
        for i in range(len(result)):
            dict_ele_size = {}
            for j in range(len(result[i])):
                try:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] += 1
                except:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] = 1
            result[i] = dict_ele_size
        return result

    def _expInvalid_power(self, exp1, exp2):
        key = dict()
        for i in range(0, len(exp1), 2):
            key[exp1[i]] = 1
        for i in range(0, len(exp2), 2):
            try:
                key[exp2[i]] += 1
                return False
            except:
                pass
        return True

    def _creatElement_power(self, multi, divide):
        '''
        multi: bậc của tử số trong công thức con
        divide: bậc của mẫu số trong công thức con
        result: list các công thức có cấu trúc multi/divide

        return: result
        '''
        key = {}
        for i in range(len(self._alpha_power)):
            key[self._alpha_power[i]] = i+1
        exp_multi = [list(self._alpha_power)]
        n = max(multi, divide)
        while len(exp_multi) < n:
            exp_multi.append([])
            for i in range(len(exp_multi[-2])):
                for j in range(key[exp_multi[-2][i][-1]] - 1, len(self._alpha_power)):
                    exp_multi[-1].append(exp_multi[-2][i]+"*"+self._alpha_power[j])
        if divide == 0:
            return exp_multi[multi-1]
        exp_divide = list(map(lambda x: x.replace("*", "/"), exp_multi[divide-1]))
        exp_multi = exp_multi[multi-1]
        result = []
        
        for i in range(len(exp_multi)):
            for j in range(len(exp_divide)):
                if self._expInvalid_power(exp_multi[i], exp_divide[j]):
                    result.append(exp_multi[i] + "/" + exp_divide[j])
        return result

    def _crElement_power(self, elements, times):
        '''
        hàm này cập nhật các công thức ghép được vào thuộc tính _result_power
        elements: list các công thức có cấu trúc multi/divide
        '''
        if len(self._index_vetcan_power) == times:
            self._result_power.append(self._element_power)
        else:
            if len(self._index_vetcan_power) == 0:
                start = 0
            else:
                start = self._index_vetcan_power[-1]
            last_op_psedou = self._last_op_power
            for i in range(start, len(elements)):
                for op in ['+', '-']:
                    if i == start and op != self._last_op_power and self._last_op_power != "":
                        continue
                    else:
                        self._element_power += op + elements[i]
                        self._index_vetcan_power.append(i)
                        self._last_op_power = op
                        self._crElement_power(elements, times)
                        self._element_power = self._element_power[:len(self._element_power)-len(elements[0])-1]
                        self._index_vetcan_power.pop()
                        self._last_op_power = last_op_psedou

    def _auto_code_power(self, elements, exp, power, list_power):
        if len(exp) == len(elements):
            self._index_ht_power += 1
            if self._index_ht_power >= self._index_qk_power:
                ct = f'({"".join(exp)}){"/A" * power}'
                p = self.get_profit(ct)
                if p > self._profit_condition:
                    self._high_profit.append(p)
                    self._exp_high_profit.append(ct)
                    if len(self._exp_high_profit) > self._number_ct:
                        raise Exception('Target Complete')

        else:
            n = len(exp)
            for i in range(len(elements[n])):
                exp.append(elements[n][i])
                power = list_power[n]
                self._auto_code_power(elements, exp, power, list_power)
                exp.pop()

    def _create_Exp_power(self):
        # print(self._n, self._index_file_qk_power, self._index_ht_power , self._index_qk_power)
        list_size = self._processListSize_power(self._preProcessListSize_power(self._get_same_even_odd_power(self._process_result_size_Element_power(self._size_Element_power([], [], self._n)))))
        list_exp_child = []
        for i in range(self._index_file_qk_power, len(list_size)):
            # print(self._n, self._index_file_qk_power, self._index_file_power, self._index_ht_power , self._index_qk_power)
            list_power = []
            for key, value in list_size[i].items():
                key = key.split('_')
                self._crElement_power(self._creatElement_power(int(key[0]), int(key[1])), value)
                power = int(key[0]) - int(key[1])
                list_power.append(power)
                list_exp_child.append(self._result_power.copy())
                self._result_power = []
                self._element_power = ''
                self._index_power = []
                self._last_op_power = ''
            self._result = []
            try:
                self._auto_code_power(list_exp_child, [], 0, list_power)
            except:
                raise Exception('Đã sinh đủ công thức theo yêu cầu')
            list_exp_child = []
            self._index_file_power += 1
            self._index_ht_power = 0
            self._index_qk_power = 0
        self._n += 1
        self._index_ht_power = 0
        self._index_qk_power = 0
        self._index_file_qk_power = 0
        return "DONE"
    
    def _save_process_power(self):
        if self._index_ht_power > 0:
            self._index_ht_power -= 1
        
        size = min(len(self._high_profit), len(self._exp_high_profit))
        self._high_profit = self._high_profit[:size]
        self._exp_high_profit = self._exp_high_profit[:size]
        if len(self._high_profit) != 0:
            self._count += 1
            df = pd.DataFrame({'profit':self._high_profit, 'fomula':self._exp_high_profit})
            df.to_csv(f"{self.path}/high_profit{self._count}.csv", index=False)
        df = pd.DataFrame({'index':[self._index_ht_power], 'index_file':[self._index_file_power], 'n': [self._n], 'count':[self._count]}) 
        df.to_csv(f"{self.path}/index.csv")

    def _update_last_time_power(self):
        try:
            self._index_qk_power = int(pd.read_csv(f'{self.path}/index.csv')['index'][0])
            self._index_file_qk_power = int(pd.read_csv(f'{self.path}/index.csv')['index_file'][0])
            self._count =  int(pd.read_csv(f'{self.path}/index.csv')['count'][0])
            self._n =  int(pd.read_csv(f'{self.path}/index.csv')['n'][0])
        except:
            pass
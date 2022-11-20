import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean

from vis_package.method_test import Method


class Complete(Method):
    def __init__(self) -> None:
        Method.__init__(self)
        self._alpha_complete = ''
        self._index_file_complete = 0
        self._index_file_qk_complete = 0
        self._index_ht_complete = 0
        self._index_qk_complete = 0
        self._result_complete = []
        self._index_complete = []
        self._index_vetcan_complete = []
        self._element_complete = ""
        self._last_op_complete = ""
        self._n = 1

    def _sizeElement_complete(self, listSizeEle, sizeEle, total_size):
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
                    self._sizeElement_complete(
                        listSizeEle, sizeEle, total_size)
                    sizeEle.pop()
            else:
                if len(sizeEle) % 2 == 1:
                    for i in range(total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement_complete(
                            listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
                else:
                    for i in range(1, total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement_complete(
                            listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
        return listSizeEle

    def _process_result_ListSize_complete(self, listSizeEle):
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

    def _creatElement_complete(self, multi, divide):
        key = {}
        for i in range(len(self._alpha_complete)):
            key[self._alpha_complete[i]] = i+1
        exp_multi = [list(self._alpha_complete)]
        n = max(multi, divide)
        while len(exp_multi) < n:
            exp_multi.append([])
            for i in range(len(exp_multi[-2])):
                for j in range(key[exp_multi[-2][i][-1]] - 1, len(self._alpha_complete)):
                    exp_multi[-1].append(exp_multi[-2][i]+"*"+self._alpha_complete[j])
        if divide == 0:
            return exp_multi[multi-1]
        exp_divide = list(map(lambda x: x.replace("*", "/"), exp_multi[divide-1]))
        exp_multi = exp_multi[multi-1]
        result = []
        for i in range(len(exp_multi)):
            for j in range(len(exp_divide)):
                if self._expInvalid_complete(exp_multi[i], exp_divide[j]):
                    result.append(exp_multi[i] + "/" + exp_divide[j])
        return result

    def _expInvalid_complete(self, exp1, exp2):
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

    def _crElement_complete(self, elements, times):
        if len(self._index_vetcan_complete) == times:
            self._result_complete.append(self._element_complete)
        else:
            if len(self._index_vetcan_complete) == 0:
                start = 0
            else:
                start = self._index_vetcan_complete[-1]
            last_op_psedou = self._last_op_complete
            for i in range(start, len(elements)):
                for op in ['+', '-']:
                    if i == start and op != self._last_op and self._last_op != "":
                        continue
                    else:
                        self._element_complete += op + elements[i]
                        self._index_vetcan_complete.append(i)
                        self._last_op_complete = op
                        self._crElement_complete(elements, times)
                        self._element = self._element[:len(self._element_complete)-len(elements[0])-1]
                        self._index_vetcan_complete.pop()
                        self._last_op_complete = last_op_psedou

    def _auto_code_complete(self, elements, exp):
        if len(exp) == len(elements):
            self._index_ht_complete += 1
            if self._index_ht_complete >= self._index_qk_complete:
                ct = "".join(exp)
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
                self._auto_code_complete(elements, exp)
                exp.pop()

    def _creat_Exp_complete(self):
        list_size = self._process_result_ListSize_complete(self._sizeElement_complete([], [], self._n))
        list_exp_child = []
        for i in range(self._index_file_qk_complete, len(list_size)):
            for key, value in list_size[i].items():
                key = key.split('_')
                self._crElement_complete(self._creatElement_complete(int(key[0]), int(key[1])), value)
                list_exp_child.append(self._result_complete.copy())
                self._result_complete = []
                self._element_complete = ""
                self._index_vetcan_complete = []
                self._last_op_complete = ""
            self._result_complete = []
            try:
                self._auto_code_complete(list_exp_child, [])
            except:
                raise Exception('Đã sinh đủ công thức theo yêu cầu')
            list_exp_child = []
            self._index_file_complete += 1
            self._index_ht_complete = 0
            self._index_qk_complete = 0
        self._n += 1
        self._index_ht_complete = 0
        self._index_qk_complete = 0
        self._index_qk_complete = 0
        return "DONE"

    def _save_process_complete(self):
        if self._index_ht_complete > 0:
            self._index_ht_complete -= 1
        
        size = min(len(self._high_profit), len(self._exp_high_profit))
        self._high_profit = self._high_profit[:size]
        self._exp_high_profit = self._exp_high_profit[:size]
        if len(self._high_profit) != 0:
            self._count += 1
            df = pd.DataFrame({'profit':self._high_profit, 'fomula':self._exp_high_profit})
            df.to_csv(f"{self.path}/high_profit{self._count}.csv", index=False)
        df = pd.DataFrame({'index':[self._index_ht_complete], 'index_file':[self._index_file_complete], 'n': [self._n], 'count':[self._count]}) 
        df.to_csv(f"{self.path}/index.csv")

    def _update_last_time_complete(self):
        try:
            self._index_qk_complete = int(pd.read_csv(f'{self.path}/index.csv')['index'][0])
            self._index_file_qk_complete = int(pd.read_csv(f'{self.path}/index.csv')['index_file'][0])
            self._count =  int(pd.read_csv(f'{self.path}/index.csv')['count'][0])
            self._n =  int(pd.read_csv(f'{self.path}/index.csv')['n'][0])
        except:
            pass

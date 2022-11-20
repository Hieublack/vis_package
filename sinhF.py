import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean

from vis_package.method_test import Method


class sinhF(Method):
    def __init__(self) -> None:
        Method.__init__(self)
        self._alpha_F = ''
        self._dtFn = pd.DataFrame()
        self._maxpf = 0
        self._index_F = 0   
        self._index = 0
        self._index_ht_F = 0
        self._F0 = None
        self._Fn = None
        self._flag = True
        self._expFn = []
        self._pfFn = []

        self._n = 1

    def _crElement_create_F(self):
        dict_key = {}
        for i in range(len(self._alpha_F)):
            dict_key[self._alpha_F[i]] = i+1
        res_exp = [list(self._alpha_F)]
        while len(res_exp) < self._n:
            res_exp.append([])
            for i in range(len(res_exp[-2])):
                if len(res_exp) == 2:
                    last_op = '+'
                else:
                    last_op = res_exp[-2][i][-2]
                for j in range(dict_key[res_exp[-2][i][-1]]-1, len(dict_key)):
                    for op in ['+', '-']:
                        if j == dict_key[res_exp[-2][i][-1]]-1 and op != last_op:
                            # print(j, dict_key[res_exp[-2][i][-1]]-1)
                            pass
                        else:
                            res_exp[-1].append(res_exp[-2][i]+op+res_exp[0][j])
        return res_exp[-1]

    def _F(self):
        res_exp = self._crElement_create_F()
        s_pf = []
        s_exp = []
        for i in range(len(res_exp)):
            for j in range(len(res_exp)):
                if i != j:
                    if self._n == 1:
                        exp = res_exp[i] + '/' + res_exp[j]
                        p = self.get_profit(exp)
                        s_exp.append(exp)
                        s_pf.append(p)

                        if p > self._profit_condition:
                            self._high_profit.append(p)
                            self._exp_high_profit.append(exp)
                            if len(self._exp_high_profit) > self._number_ct:
                                raise Exception('Target Complete')
                
                    else:
                        exp = f"({res_exp[i]})/({res_exp[j]})"
                        p = self.get_profit(exp)
                        s_exp.append(exp)
                        s_pf.append(p)

                        if p > self._profit_condition:
                            self._high_profit.append(p)
                            self._exp_high_profit.append(exp)
                            if len(self._exp_high_profit) > self._number_ct:
                                raise Exception('Target Complete')
        
        df = pd.DataFrame({'congthuc' : s_exp, 'profit': s_pf})
        df.to_csv(f'{self.path}/f0.csv', index=False)

        df = pd.DataFrame({'n': [0], 'mpf': [max(s_pf)]})
        df.to_csv(f'{self.path}/fn.csv', index=False)

        df = pd.DataFrame({'index' : [0]})
        df.to_csv(f'{self.path}/indexF.csv', index=False)

        df = pd.DataFrame({'index_file': [0]})
        df.to_csv(f'{self.path}/index_file.csv', index=False)
        return "DONE F0"

    def _save_F0(self):
        try:
            self._dtFn = pd.read_csv(f'{self.path}/f0.csv')
        except:
            self._n = 1
            self._F()
            print('DONE save F0')

    def _read_file(self):
        try:
            self._index_F = int(pd.read_csv(f'{self.path}/indexF.csv')['index'][0])
            self._maxpf = float(pd.read_csv(f'{self.path}/fn.csv')['mpf'][0])
            self._n = int(pd.read_csv(f'{self.path}/fn.csv')['n'][0])
            self._F0 = list(pd.read_csv(f'{self.path}/f0.csv')['congthuc'])
            self._Fn = list(pd.read_csv(f'{self.path}/f{self._n}.csv')['congthuc'])
        except:
            raise Exception("Kết thúc vì quy trình xảy ra gián đoạn!")

    def _save_file(self):
        self._expFn = self._expFn[:min(len(self._expFn), len(self._pfFn))]
        self._pfFn = self._pfFn[:min(len(self._expFn), len(self._pfFn))]

        if len(self._expFn) != 0:
            df = pd.DataFrame({'index': [self._index_ht_F]})
            df.to_csv(f'{self.path}/indexF.csv', index=False)

            try:
                self._dtFn = pd.read_csv(f'{self.path}/f{self._n+1}.csv')
                self._expFn = list(self._dtFn['congthuc']) + self._expFn
                self._pfFn = list(self._dtFn['profit']) + self._pfFn
            except:
                pass
            finally:
                self._dtFn = pd.DataFrame({'congthuc': self._expFn, 'profit': self._pfFn})
                self._dtFn.to_csv(f'{self.path}/f{self._n+1}.csv', index=False)

            if self._flag:
                df = pd.DataFrame({'n': [self._n+1], 'mpf': [max(self._pfFn)]})
                df.to_csv(f'{self.path}/fn.csv', index=False)
                self._flag = False
            df = 0
        
        else:
            return "........"
        return "DONE SAVE FILE"

    def _auto_code_F(self):
        while True:
            for i in range(self._index_F, len(self._Fn)): 
                for j in range(self._index_F, len(self._F0)):
                    for op in ['+', '-', '*']:
                        if self._index_ht_F >= self._index_F:
                            exp = self._Fn[i] + op + self._F0[j]
                            p = self.get_profit(exp)
                            #cao hơn max_pf thì lưu để tạo F(n+1)
                            if p > self._maxpf:
                                self._expFn.append(exp)
                                self._pfFn.append(p)
                            if p > self._profit_condition:
                                self._high_profit.append(p)
                                self._exp_high_profit.append(exp)
                                if len(self._exp_high_profit) > self._number_ct:
                                    raise Exception('Target Complete')
                self._index_ht_F += 1
                self._index_F = 0
            self._flag = True
            self._index_ht_F = 0
            if self._save_file() != "DONE SAVE FILE":
                print('STOP')
                raise Exception('DONE SINH F')
            
            self._expFn = []
            self._pfFn = []
            self._index_ht_F = 0
            self._index_F = 0
            try:
                self._read_file()
            except:
                break

    def _save_process_F(self):
        if self._index_ht_F > 0:
            self._index_ht_F -= 1
        
        size = min(len(self._high_profit), len(self._exp_high_profit))
        self._high_profit = self._high_profit[:size]
        self._exp_high_profit = self._exp_high_profit[:size]
        if len(self._high_profit) != 0:
            self._count += 1
            df = pd.DataFrame({'profit':self._high_profit, 'fomula':self._exp_high_profit})
            df.to_csv(f"{self.path}/high_profit{self._count}.csv", index=False)
        



import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean 
from vis_package.sinhF import sinhF
from vis_package.power_method import Power
from vis_package.complete_method import Complete

class VIS(Power, Complete, sinhF):
    def __init__(self) -> None:
        Power.__init__(self)
        Complete.__init__(self)
        sinhF.__init__(self)


    def create_exp_option(self, time_moment, number_fomula = 5000, profit_condition = 1.4, method = 'complete', module = 'basic'):
        '''
        time_moment:        số năm muốn test
        number_ct:          số công thức muốn lấy
        profit_condition:   lợi nhuận tối thiểu công thức muốn lấy
        '''
        if module == 'basic':
            self.get_profit = self.get_profit_basic
            self.data_full = self.data_full.sort_values(by=['TIME', 'PROFIT'], ascending=[False, False], ignore_index=True)
        elif module == 'average_r_rank':
            print(module)
            self.get_profit = self.get_min_sum_delta_rank
            self.data_full = self.data_full.sort_values(by=['TIME', 'PROFIT'], ascending=[False, False], ignore_index=True)
        else:
            self.data_full = self.data_full.sort_values(by=['TIME', 'PROFIT'], ascending=[False, False], ignore_index=True)
            if module == 'rank':
                self.get_profit = self.get_profit_harmean_rank
            else:
                self.get_profit = self.get_profit_RankCorrelation
        self._time_moment = time_moment
        self._number_ct = number_fomula
        self._profit_condition = profit_condition
        self._index_T = self._get_index_T()
        self.data_test = self.data_full.loc()[self._index_T[-self._time_moment]:self._index_T[-1]].reset_index(drop=True)
        self._index_test = self._get_index_T(for_data= 'test')
        self._len_data_i = []
        for i in range(1, len(self._index_test)):
            self._len_data_i.append(self._index_test[i]-self._index_test[i-1])
        self.get_variable()
        # print('DONE đọc biến', self._alpha, self._alpha_power)
        self._run(method)
        
        if method == 'complete':
            print('lưu complete')
            self._save_process_complete()
        elif method == 'power':
            print('lưu power')
            self._save_process_power()
        elif method == 'sinhF':
            print('lưu sinhF')
            self._save_file()
            self._save_process_F()

        file_fomula = pd.DataFrame({'fomula': self._exp_high_profit, 'profit': self._high_profit})

        return file_fomula

    def _run(self, method):
        if method == 'complete':
            self._update_last_time_complete()
            print('chạy complete')
            self._alpha_complete = self._alpha
            while True:
                try:
                    self._index_file_complete = self._index_file_qk_complete
                    self._creat_Exp_complete()
                except:
                    break
        elif method == 'sinhF':
            print('chạy sinh F')
            self._alpha_F = self._alpha
            try:
                self._alpha_F = self._alpha_F.replace('N', '')
            except:
                pass
            self._save_F0()
            self._read_file()
            while True:
                try:
                    self._auto_code_F()
                except:
                    print('STOP')
                    break
        elif method == 'power':
            self._update_last_time_power()
            print('chạy power')
            self._alpha_power = self._alpha.replace('A', '')

            while True:
                try:
                    self._index_file_power = self._index_file_qk_power
                    self._create_Exp_power()
                except:
                    break


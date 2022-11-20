import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean


class Method():
    def __init__(self) -> None:
        self.path = ''
        self._alpha = ''
        self.data_full = pd.DataFrame()
        self.data_test = pd.DataFrame()
        self._high_profit = []
        self._exp_high_profit = []
        self._number_ct = math.inf
        self._profit_condition = 0
        self._index_T = []  
        self._index_test = []
        self._time_moment = 0
        self._count = 0
        self._len_data_i = []
    
    def get_profit(self, fomula):
        return np.random.randint(1,10000)

    def get_variable(self):
        global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, PROFIT, COMPANY
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = [[]]*26
        list_variable = [[]]*26
        list_column = list(self.data_test.columns)
        for i in range(4, len(list_column)):
            list_variable[i-4] = np.array(self.data_test[list_column[i]])
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = list_variable
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])
        var_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        count = 0
        for var in [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]:
            if len(var) > 0:
                self._alpha = self._alpha + var_char[count]
            count += 1
        # return list_variable

    def _getIndex(self):
        arr = np.array(self.data_full['TIME'])
        for s in arr:
            yield (int(s)-np.min(arr))+1

    def _get_index_T(self, for_data = 'full'):
        if for_data == 'full':
            list_T = self.data_full['TIME']
            index_T = [0]
            for i in range(len(list_T)-1):
                if list_T[i] != list_T[i+1]:
                    index_T.append(i+1)
            index_T.append(len(list_T))
            return index_T
        else:
            list_T = self.data_test['TIME']
            index_T = [0]
            for i in range(len(list_T)-1):
                if list_T[i] != list_T[i+1]:
                    index_T.append(i+1)
            index_T.append(len(list_T))
            return index_T

    def ReLU(self, x):
        return x * (x > 0)
    
    def get_min_sum_delta_rank(self, fomula):
        result_ =  np.nan_to_num(eval(fomula), nan=-np.inf, posinf=-np.inf, neginf=-np.inf)
        rank = []
        for j in range(len(self._index_test)-1, 0, -1):
            top2 = heapq.nlargest(2,result_[self._index_test[j-1]:self._index_test[j]])         #lấy top 2 giá trị lớn nhất
            if top2[0] == top2[1] or np.max(result_[self._index_test[j-1]:self._index_test[j]]) == np.min(result_[self._index_test[j-1]:self._index_test[j]]):
                return 0
            rank_thuc = np.argsort(-result_[self._index_test[j-1]:self._index_test[j]]) + 1
            # print(rank_thuc)
            num_company = len(-result_[self._index_test[j-1]:self._index_test[j]])
            rank_goc = np.arange(1, num_company + 1)
            # print(rank_goc)
            delta_rank = ((rank_thuc - rank_goc)/num_company)**2        
            rank.append(np.sum(delta_rank)/num_company)
        average_delta_rank =  1 - np.average(rank)
        return average_delta_rank

    def get_profit_RankCorrelation(self, fomula):
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        rank_pro = []
        for j in range(len(self._index_test)-1, 0, -1):
            top2 = heapq.nlargest(2,result_[self._index_test[j-1]:self._index_test[j]])         #lấy top 2 giá trị lớn nhất
            if top2[0] == top2[1] or np.max(result_[self._index_test[j-1]:self._index_test[j]]) == np.min(result_[self._index_test[j-1]:self._index_test[j]]):
                return 0
            n_comp = len(result_[self._index_test[j-1]:self._index_test[j]])
            rank_cthuc = np.arange(1, n_comp+1)
            rank_thuc = np.argsort(-result_[self._index_test[j-1]:self._index_test[j]]) + 1
            a_i = np.sum(self.ReLU((rank_cthuc - rank_thuc)**2))
            result_exp = 1 - 6*a_i/(n_comp*(n_comp**2 - 1))
            rank_pro.append(result_exp)
        average_rank = np.average(rank_pro)
        return average_rank

    def get_profit_harmean_rank(self, fomula):
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        rank = []
        for j in range(len(self._index_test)-1, 0, -1):
            top2 = heapq.nlargest(2,result_[self._index_test[j-1]:self._index_test[j]])         #lấy top 2 giá trị lớn nhất
            if top2[0] == top2[1] or np.max(result_[self._index_test[j-1]:self._index_test[j]]) == np.min(result_[self._index_test[j-1]:self._index_test[j]]):
                return 0
            rank_i = np.argmax(result_[self._index_test[j-1]:self._index_test[j]]) + 1           
            rank.append(self._len_data_i[j-1]/rank_i)
        hmean_rank = hmean(rank)
        return hmean_rank

    def get_profit_basic(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = 1
        for j in range(len(self._index_test)-1, 0, -1):
            top2 = heapq.nlargest(2,result_[self._index_test[j-1]:self._index_test[j]])         #lấy top 2 giá trị lớn nhất
            if top2[0] == top2[1] or np.max(result_[self._index_test[j-1]:self._index_test[j]]) == np.min(result_[self._index_test[j-1]:self._index_test[j]]):
                return 0
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            loinhuan*= PROFIT[index_max]
        return loinhuan**(1.0/(self._time_moment-1))

    def get_value_profit_company(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = []
        company = []
        value = []
        year = []
        rank_index = []
        for j in range(len(self._index_test)-1, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            rank_index.append(np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+1)
            loinhuan.append(PROFIT[index_max])
            company.append(COMPANY[index_max])
            value.append(result_[index_max])
            year.append(self.data_test['TIME'][index_max])
        return value, loinhuan, company, year, rank_index

    def get_value_profit_company_RankCorrelation(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = []
        company = []
        value = []
        year = []
        rank_index = []
        
        for j in range(len(self._index_test)-1, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            rank_index.append(np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+1)
            loinhuan.append(PROFIT[index_max])
            company.append(COMPANY[index_max])
            n_comp = len(result_[self._index_test[j-1]:self._index_test[j]])
            rank_cthuc = np.arange(1, n_comp+1)
            rank_thuc = np.argsort(-result_[self._index_test[j-1]:self._index_test[j]]) + 1
            a_i = np.sum(self.ReLU((rank_cthuc - rank_thuc)**2))
            result_exp = 1 - 6*a_i/(n_comp*(n_comp**2 - 1))
            value.append(result_exp)
            year.append(self.data_test['TIME'][index_max])
        return value, loinhuan, company, year, rank_index

    def get_value_profit_company_911(self, fomula):
        # self.get_variable()
        print(fomula)
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = []
        company = []
        value = []
        year = []
        rank_index = []
        number_comp_curent = []
        list_rank_not_invest_ct = []
        LIST_RANK_NOT_INVEST = self.get_rank_not_invest()
        for j in range(len(self._index_test)-1, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            rank_index.append(np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+1)
            number_comp_curent.append(len(result_[self._index_test[j-1]:self._index_test[j]]))
            loinhuan.append(PROFIT[index_max])
            company.append(COMPANY[index_max])
            value.append(result_[index_max])
            year.append(self.data_test['TIME'][index_max])

            id_not_invest = LIST_RANK_NOT_INVEST[-j] 
            rank_thuc = np.argsort(-result_[self._index_test[j-1]:self._index_test[j]]) + 1
            list_rank_not_invest_ct.append(np.where(rank_thuc == id_not_invest)[0][0]+1)
        return value, loinhuan, company, year, rank_index, number_comp_curent, list_rank_not_invest_ct
    
    def get_rank_not_invest(self):
        list_rank_ko_dau_tu = []
        COMPANY_CURENT = self.data_test['SYMBOL']
        for j in range(len(self._index_test)-1, 0, -1):
            # profit_q = PROFIT[index_test[j-1]:index_test[j]]
            COMP = COMPANY_CURENT[self._index_test[j-1]:self._index_test[j]]
            list_rank_ko_dau_tu.append(np.where(COMP == 'NOT_INVEST')[0][0]+1)
        return np.array(list_rank_ko_dau_tu)















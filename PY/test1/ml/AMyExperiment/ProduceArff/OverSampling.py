import numpy as np
from sklearn.neighbors import NearestNeighbors

class myOverSampling:
    def __init__(self,radio='minority'):
        self.radio = radio
    def _statDiscre(self,X_train,y_train):
        from sklearn import preprocessing


        X = X_train
        y = np.array(y_train)

        scaler = preprocessing.MinMaxScaler()
        X = scaler.fit_transform(X)
        posi_Y_sum = np.sum(np.array(y)=='Y')
        # neg_Y_sum = np.sum(y=='N')
        pos_X = []
        org_X = []
        # neg_X = []
        a,b = np.shape(X)
        pos_X_sum = np.zeros(b)
        # neg_X_sum = np.zeros(b)
        for i,yi in enumerate(y):
            if yi == 'Y':
                pos_X.append(X[i])
                org_X.append(X_train[i])
                pos_X_sum+=X[i]
        #     else:
        #         neg_X.append(X[i])
        #         neg_X_sum+=X[i]
        # neg_X = np.array(neg_X)
        pos_X = np.array(pos_X)
        pos_m = pos_X_sum/posi_Y_sum
        # neg_m = neg_X_sum/neg_Y_sum
        tmp_X = pos_X-pos_m
        disc_X = np.dot(tmp_X.T,tmp_X)
        end_X = []
        for i in pos_X:
            end_X.append(np.dot(np.dot(i,disc_X),i.T))
        return org_X,pos_X,end_X/np.sum(end_X)


    def _genNeigMat(self,pos_X, K):
        neig = NearestNeighbors(n_neighbors=K)
        neig.fit(pos_X)
        # print(np.shape(pos_X))

        return neig.kneighbors(pos_X)[1]


    def _genPerPoint(self,p1, p2, beta,X_train):
        p1 = np.array(p1)
        p2 = np.array(p2)
        n = np.shape(X_train)[1]
        betas = np.random.rand(n) * beta  # 使新点不在p1,p2连线上
        tmp_dis = (p2 - p1) * betas
        return p1 + tmp_dis
    def _genPosByDis(self,pn,beta,X_train,y_train):
        posNum = np.sum(np.array(y_train)=='Y')
        negNum = np.sum(np.array(y_train)=='N')
        posGenNum = negNum*pn-posNum  #Y/N == pn时 所需要生成Y类的数目
        org_X,pos_X,dis = self._statDiscre(X_train,y_train)

        dis_num = np.around(dis*posGenNum)
        dis_max = int(np.max(dis_num))
        # dis_num.sort()
        # print(np.sum(dis_num),np.shape(X_train))
        # print(np.argwhere(dis_num>0))
        # print(np.shape(pos_X),np.shape(dis_num))
        _K = 10 # 控制近邻数
        _K = min(min(dis_max+1,_K),posNum)
        neigs = self._genNeigMat(pos_X,_K)
        # print(neigs)
        gen_pos = []
        # print(dis_num)
        # dis_all = np.sum(dis_num)

        # dis_gt_K = np.argwhere(dis_num>_K)
        # plus_gen_num = 0
        # for idx in dis_gt_K:
        #     plus_gen_num+=(dis_num[idx[0]]-_K)
        # per_plus = plus_gen_num//(len(dis_num)-len(dis_gt_K))
        # new_dis_num = dis_num+per_plus
        # print(new_dis_num)
        for i,e in enumerate(dis_num):
            j = 1
            while j<=e:
                # print(i,"--",j)
                gen_pos.append(self._genPerPoint(org_X[i],org_X[neigs[i][j%_K]],beta,X_train))
                j+=1
        y_lable = ['Y']*len(gen_pos)
        return gen_pos,y_lable

    def _ennClearn(self,X,y,k1=7,k2=10):
        neig = self._genNeigMat(X,k2+1)
        newX = []
        newY = []
        for i,e in enumerate(neig):
            j = 1
            count=0
            while j<=k2:
                if y[e[j]] != y[i]:
                    count+=1
                j+=1
            if count<k1:
                newX.append(X[i])
                newY.append(y[i])
        return newX,newY
    def fit_sample(self,X,y):
        ps, py = self._genPosByDis(1, .125,X,y)
        ps.extend(X)
        py.extend(y)
        newX, newY = self._ennClearn(ps, py)
        return newX,newY

if __name__ == '__main__':
    print(1)

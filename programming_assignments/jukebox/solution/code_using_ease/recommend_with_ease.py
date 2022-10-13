import pandas as pd
from scipy.sparse import csr_matrix
import numpy as np
import sys


def gen_top_reco(X, lamb=10.0, K=100, target_user_inds=None):
    G = (X.T @ X).toarray()
    diags = np.diag_indices(G.shape[0])
    G[diags] += lamb
    P = np.linalg.inv(G)
    B = P / -np.diag(P)
    _X = X
    if target_user_inds is not None:
        _X = X[target_user_inds, :]
    scores = _X @ B
    scores = np.asarray((scores - _X.astype(bool).astype(int) * 10000))
    top_reco = (-scores).argsort(-1)[:, :K]
    return top_reco


listen_count_fname, user_ids_fname, K = sys.argv[1], sys.argv[2], int(sys.argv[3])

with open(user_ids_fname, 'r') as f:
    target_user_ids = f.read().strip().split()
tr = pd.read_csv(listen_count_fname, sep=' ', header=None, dtype=str)
tr.columns = ['uid', 'sid', 'cnt']
tr['cnt'] = tr['cnt']
uid2idx = {_id: i for (i, _id) in enumerate(tr.uid.unique())}
sid2idx = {_id: i for (i, _id) in enumerate(tr.sid.unique())}
idx2uid = {i: _id for (_id, i) in uid2idx.items()}
idx2sid = {i: _id for (_id, i) in sid2idx.items()}
tr['uidx'] = tr.uid.apply(lambda x: uid2idx[x])
tr['sidx'] = tr.sid.apply(lambda x: sid2idx[x])
n_user, n_item = len(uid2idx), len(sid2idx)
with open('./user_id.txt', 'w') as f:
    print('\n'.join(tr.uid.tolist()), file=f)

X = csr_matrix((tr.cnt, (tr.uidx, tr.sidx)),
               shape=(n_user, n_item),
               dtype=np.float32)
X.data[:] = 1.0 + np.log(1.0 + X.data[:])

target_user_inds = [uid2idx[uid] for uid in target_user_ids]
top_reco = gen_top_reco(X, lamb=30.0, K=K,
                        target_user_inds=target_user_inds)

for uid, rec_list in zip(target_user_ids, top_reco):
    rec_sids = [str(idx2sid[sidx]) for sidx in rec_list]
    print(uid, ' '.join(rec_sids))

import pandas as pd
from scipy.sparse import csr_matrix
import numpy as np
from jax import grad, jit
import jax.numpy as jnp

import sys


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
    print('\n'.join(tr.uid.unique()), file=f)

X = csr_matrix((tr.cnt, (tr.uidx, tr.sidx)),
               shape=(n_user, n_item),
               dtype=np.float32)
X.data[:] = 1.0 + np.log(1.0 + X.data[:])

jX = jnp.array(X.todense())
P = jnp.array(np.random.normal(0, 0.001, size=(n_item, n_item)))
P = P.at[jnp.diag_indices(P.shape[0])].set(0)


@jit
def loss_fn(X, P):
    ret = (((X - X @ P) **2).sum() / X.shape[0])
    ret = ret
    return ret


@jit
def loss_fn_with_reg(X, P):
    ret = loss_fn(X, P)
    ret = ret + 0.01 * (P * P).sum()
    return ret

grad_fn = grad(loss_fn_with_reg, argnums=1)
lr = 0.06
for i in range(100):
    batch = np.random.choice(X.shape[0], 512)
    r = grad_fn(jX[batch], P)
    P -= lr * r
    P = P.at[jnp.diag_indices(P.shape[0])].set(0)
    lr *= 0.99

target_user_inds = [uid2idx[uid] for uid in target_user_ids]
scores = X[target_user_inds] @ np.array(P)
scores = np.asarray(scores - X[target_user_inds].astype(bool).astype(int) * 10000)
top_reco = (-scores).argsort(-1)[:, :K]

for uid, rec_list in zip(target_user_ids, top_reco):
    rec_sids = [str(idx2sid[sidx]) for sidx in rec_list]
    print(uid, ' '.join(rec_sids))

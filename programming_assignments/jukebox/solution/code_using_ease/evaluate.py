#!/Users/ita/opt/anaconda3/bin/python
import math
import sys


def load_res(fname):
    ret = {}
    with open(fname, 'r') as f:
        for l in f:
            l = l.strip().split()
            uid, sids = l[0], l[1:]
            ret[uid] = sids
    return ret


def ndcg(recs, gt):
    Q, S = 0.0, 0.0
    for u, vs in gt.items():
        rec = recs.get(u, [])
        if not rec:
            continue

        idcg = sum([1.0 / math.log(i + 2, 2) for i in range(len(vs))])
        dcg = 0.0
        for i, r in enumerate(rec):
            if r not in vs:
                continue
            rank = i + 1
            dcg += 1.0 / math.log(rank + 1, 2)
        ndcg = dcg / idcg
        S += ndcg
        Q += 1
    return S / Q


rec_fname, gt_fname = sys.argv[1], sys.argv[2]

recs = load_res(rec_fname)
gt = load_res(gt_fname)
print("NDCG:", ndcg(recs, gt))

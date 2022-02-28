import math


def ndcg(gt, rec):
    idcg = sum([1.0 / math.log(i + 2, 2) for i in range(len(gt))])
    dcg = 0.0
    for i, r in enumerate(rec):
        if r not in gt:
            continue
        gt_index = gt.index(r)
        if i != gt_index:
            rel = 0.7
        else:
            rel = 1.0
        dcg += rel / math.log(i + 2, 2)
    ndcg = dcg / idcg

    return ndcg

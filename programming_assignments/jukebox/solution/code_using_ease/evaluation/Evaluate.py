#-*- coding: utf8 -*-
import re
import sys
import math
import logging


NUM_ITEMS = 1078898


class Metric:
    @staticmethod
    def mrr(recs, db):
        Q = 0
        S = 0
        for u, vs in db.items():
            Q += 1
            min_rank = -1
            for v, s in vs.items():
                rec = recs.get(u, [])
                rank = [i + 1 for i in range(len(rec)) if rec[i][0] == v]
                if rank:
                    #print 'hit', u, v, s, ',', rank[0], rec[rank[0] - 1][1]
                    if min_rank == -1:
                        min_rank = rank[0]
                    else:
                        min_rank = min(min_rank, rank[0])
            if min_rank > 0:
                S += 1.0 / min_rank
        if Q > 0:
            # print 'S=%f' % S
            # print 'Q=%f' % Q
            # print '%.10f' % (S / Q)
            return S / Q

    @staticmethod
    def map(recs, db):
        Q = 0
        S = 0
        for u, vs in db.items():
            N = len(vs)
            Hit = 0
            SS = 0
            set_v = set(vs.keys())
            rec = recs.get(u, [])
            for idx, r in enumerate(rec):
                if r[0] in set_v:
                    Hit += 1
                    SS += (Hit / float(idx + 1))
            SS = SS / float(N)
            S += SS
            Q += 1
        if Q > 0:
            # print 'S=%f' % S
            # print 'Q=%f' % Q
            # print '%.10f' % (S / Q)
            return S / Q

    @staticmethod
    def auc(recs, db, num_total_cand):
        Q = 0.0
        S = 0.0
        for u, vs in db.items():
            Q += 1

            rec = recs.get(u, [])

            num_dropped_items = num_total_cand - len(rec)
            num_rel_items = len([1 for r in rec if r[0] in vs])
            num_eval_items = num_total_cand
            num_eval_pairs = (num_eval_items - num_rel_items) * num_rel_items
            if num_eval_pairs == 0:
                S += 0.5
                continue

            num_correct_pairs = 0
            hit_count = 0
            for r in rec:
                if r[0] not in vs:
                    num_correct_pairs += hit_count
                else:
                    hit_count += 1

            num_missing_rel_items = len(vs) - num_rel_items
            num_correct_pairs += (hit_count * (num_dropped_items - num_missing_rel_items))
            S += float(num_correct_pairs) / float(num_eval_pairs)
        return S / Q

    @staticmethod
    def ndcg(recs, db):
        Q = 0.0
        S = 0.0
        for u, vs in db.items():

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


class Evaluation:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)-8s] %(asctime)s [%(filename)s] [%(funcName)s:%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

        fh = logging.FileHandler(self.__class__.__name__ + '.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)-8s] %(asctime)s [%(filename)s] [%(funcName)s:%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def load_database(self, fname_target_users, fname_database, has_header=False):
        self.logger.info('Loading database -> %s' % fname_database)
        self.target_users = None
        if fname_target_users:
            self.target_users = set(map(int, open(fname_target_users)))

        data = ''
        fin = open(fname_database)
        while True:
            line = fin.readline()
            if line[0] == '#':
                continue
            data += line
            break

        if has_header:
            fin.readline()

        data += fin.read()

        tokenizer = re.compile('([^ \n]+)')

        self.db = {}
        tokens = tokenizer.findall(data)
        it = iter(tokens)
        for u, i, s in zip(it, it, it):
            u, i, s = int(u), int(i), float(s)

            if self.target_users and u not in self.target_users:
                continue

            if u not in self.db:
                self.db[u] = {}

            self.db[u][i] = s

    def load_test_file(self, fpath, has_header=True):
        self.logger.info('Loading database -> %s' % fpath)
        with open(fpath) as f:
            if has_header:
                f.readline()
                header = f.readline().rstrip().split(" ")
                max_uid, max_iid, num_line = map(int, header)
            td = {}
            for line in f:
                uid, iid, r = line.split(" ")
                r = float(r)
                if r > 3.0:
                    td.setdefault(uid, set()).add(iid)
        return td

    def load_topk_file(self, fpath):
        self.logger.info('Loading topk file -> %s' % fpath)
        with open(fpath) as f:
            topk = {}
            num_line = 0
            for line in f:
                num_line += 1
                item = line.strip().split(" ")
                if len(item) == 0 or not item[0].isdigit():
                    print("error %d" % num_line)
                # item = map(int, item)
                topk[item[0]] = item[1:]
        return topk

    def eval_topk(self, topk, td, metrics=[]):
        self.logger.info('Start evalution')

        scores = []
        if 'mrr' in metrics:
            self.logger.info('[MRR]')
            mrr = Metric.mrr(topk, td)
            self.logger.info('MRR: %.10f' % mrr)
            scores.append(mrr)

        if 'map' in metrics:
            self.logger.info('[MAP]')
            _map = Metric.map(topk, td)
            self.logger.info('MAP: %.10f' % _map)
            scores.append(_map)

        if 'auc' in metrics:
            self.logger.info('[AUC]')
            self.logger.info('NUM_RECOMMENDATION_CANDIDATES: %d' % NUM_ITEMS)
            auc = Metric.auc(topk, td, NUM_ITEMS)
            self.logger.info('AUC: %.10f' % auc)
            scores.append(auc)

        if 'ndcg' in metrics:
            self.logger.info('[NDCG]')
            ndcg = Metric.ndcg(topk, td)
            self.logger.info('NDCG: %.10f' % ndcg)
            scores.append(ndcg)

        self.logger.info('| ' + (' | '.join(['%.10f' % s for s in scores])) + ' |')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('python', sys.argv[0], '<test file>', '<topk_result>')
        sys.exit()
    test_fname = sys.argv[1]
    topk_fname = sys.argv[2]
    e = Evaluation()
    test_data = e.load_test_file(test_fname, has_header=False)
    print(len(test_data))
    topk = e.load_topk_file(topk_fname)
    e.eval_topk(topk, test_data, ['ndcg'])

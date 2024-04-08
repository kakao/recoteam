# Reverse Maximum Inner Product Search- How to efficiently find users who would like to buy my item?

- Paper : <https://arxiv.org/abs/2110.07131>
- Authors : Daichi Amagata, Takahiro Hara
- Reviewer : iggy.ll
- Topics
  - [#Scalable_Performance](../../topics/Scalable%20Performance.md)
  - #Inner_Product_Search
  - [#RecSys2021](RecSys2021.md)

## Summary

## Approach

### Notations

- u_i in Q (User vectors)
- p_j in P (Item vectors)
- <a, b>: dot product between a and b.

### Maximum Inner Product Search (MIPS)

Given a user u_i \in Q, Find \text{Topk}(u_i) = \text{argtopk}_{p_j \in P} <u_i, p_j>

### Reverse Inner Product Search (R-MIPS)

Given an item q \in P, Find a set of users u_i such that q \in \text{TopK}(u_i)

### Main claim

with simple preprocessing, those three questions can be answered in constant time:

1. Given query item q is included in \text{Topk}(u_i) of the user u_i
2. Given query item q is not included in \text{Topk}(u_i) of the user u_i
3. Given query item q is not included in \text{Topk}(u_i) of all users u_i of some (not any) set of users u_i, or block B.

#### Constructing Block B

1. Perform Descending Sort Q, P according to their L2 norm. i.e., \|\|u_i\|\| \geq \|\|u_j\|\| if i < j.
2. appropriately partition user vectors Q. e.g., Q = [u_1, u_2, ...,u_6], then B_1 = [u_1,u_2, u_3], and B_2 = [u_4, u_5, u_6]
3. define L_i (it is easier to write in python here)

`L_i = np.array(sorted(dot(u_i, P[:50, :]), ascending=False))`
`L(B) = np.min([L_i for u_i in B], axis=0)`
L_i is sorted values of dot products between user u_i and item vectors with top-k norms.

Claim 1. Given u_i, q, if <u_i, q> \leq L_i[k], then q \notin \text{TopK}(u_i)
proof: L_i[k] is dot product between u_i and item p such that p is in top-K ranking in norm. Thus p cannot be higher than rank k and dot product with q is lower than dot product with p. Thus q cannot be in \text{TopK}(u_i)

Claim 2. Given u_i, q, if <u_i, q> \geq \|\|u_i\|\| \|\| p_k\|\|, then q \in \text{TopK}(u_i)
proof: Let p to be a true top-k item. \|\|u_i\|\| \|\| p\|\| \geq \|\|u_i\|\| \|\| p_k\|\| \geq <u_i, q> holds. Thus q must be in top-k ranking

Claim 3. Given q, a block B and u_i is a first vector in B, \|\|u_i\|\| \|\|q\|\| \leq L(B)[k], then q \notin \text{TopK}(u_i) for all u_i \in B
proof: \max_{u_i \in B} <u_i, q> \leq \|\|u_i\|\| \|\|q\|\| \leq L(B)[k]. Then by Claim 1, it holds

### Procedure

```text
given item query vector q
ret = {}
for B in Blocks:
  if we can skip block B using Claim 3:
    continue;
  for u in B:
    if we can skip u using Claim 1:
      continue
    if u, q satisfy Claim 2:
      ret.add(u)
    else:
      let TopK(u) using exhaustie search;
      if q in TopK(u)
      ret.add(u)
return ret
```

Note:

- We can parallelize easily along with Blocks.
- Worst Case bound is equal to Exhaustive Search
- No theoretical bound is given

## Conclusion

- 생각해보면 쓰이는 수학/프로그래밍 테크 기술이 난이도가 고등학교때 기하와 벡터 배웠을 때 딱 그 정도만 쓰는 것 같은데 아이디어가 진짜 좋은 것 같습니다.
- 개선 여지가 많은 것 같다. 특히, Block Construction 부분에서, 블록 내부의 벡터들의 순서나, 블록 사이의 관계 측면에서 뭔가 개선할 여지가 있을 것 같은데 하는 생각이 듭니다. 아이디어를 일부로 약간만 풀고 세부적인 테크닉들은 공개 안 한 것 같습니다.

# Shallow AutoEncoder를 이용한 Jukebox 풀이

## 데이터 전처리

[`1. 데이터 전처리.ipynb`](1.%20데이터%20전처리.ipynb)를 참조하세요.

## 오토인코더를 이용한 추천 모델

$x$를 한 유저가 들었던 곡의 bag of words representation이라 하면,
$d = Hx, y = Gd$ where $H \in \mathbf{R}^{I \times h}, G \in \mathbf{R}^{h \times I}$ 이렇게 표현할 수  있습니다.

![오토인코더 모델](https://t1.daumcdn.net/thumb/R1280x0.fpng/?fname=http://t1.daumcdn.net/brunch/service/user/1oU7/image/2pDhz3Hm_pIZ5jZppwtiOmZYMsU.png)

y에서 점수가 높은 index의 아이템이, X가 좋아할 아이템이라 해석할 수 있고, 학습 시에는, y는 x를 reconstruct하도록 모델을 최적화할 수 있습니다($(x-y)^T(x-y)$).  
$X$를 모든 유저의 bag of words 표현의 행렬($\mathbf{R}^{u \times I}$)이라 하고, Y를 이에 따른 AutoEncoder의 reconstruction이라 합니다.

$$ L = \sum_{x_u} (x_u - y)^T(x_u - y) = (X - Y)^T(X-Y) = |X - PX|_F $$

이 모델의 학습 가능한 패러미터는 $H_1, H_2$가 되고, 다음과 같이 선언할 수 있습니다.

```python
H1 = jnp.array(np.random.normal(0, 0.001, size=(n_items, latent_dim)))
H2 = jnp.array(np.random.normal(0, 0.001, size=(n_items, latent_dim)))
```

위 $L$을, user 수에 따라 normalize하게 구현한 파이썬 구현은 다음과 같습니다.

```python
def loss_ae(X, H, G):
    Y = (G @ (H @ X))
    return ((X - Y) ** 2) / X.shape[0]
```

## 조금 더 간단한 모델

$Gd = G(Hx) = GHx$라는 점을 생각해 보면, 우리는 AutoEncoder에서 Encoder $H$와 $G$를 굳이 분리하지 않아도 괜찮다는 생각을 해 볼 수 있습니다. $P = GH$로 정의하고, 이번엔 최적화하는 패러미터가 $H$, $G$가 아니라 $P$를 최적화하는 방식을 생각해볼 수 있습니다.

$$ L = \sum_{x_u} (x_u - y)^T(x_u - y) = (X - Y)^T(X-Y) = |X - PX|_F $$

이 모델의 학습 가능한 패러미터는 $P$이며, 다음과 같이 선언할 수 있습니다.

```python
P = jnp.array(np.random.normal(0, 0.001, size=(n_items, n_items)))
```

간단한 표현의 또 다른 이점은, 우리가 조절해야 하는 하이퍼패러미터였던 $latent_dim$을 지워버릴 수 있다는 점입니다. 다만, 이 방법의 한 가지 제약사항은, P가 Identity Matrix $I$를 닮아도 로스가 0이 되어버린다는 문제가 있습니다. 따라서, $P$의 diagonal 값을 0으로 강제로 고정해주는 constraint를 줍니다. 문제를 정의하면 다음과 같습니다.

```python
X = jnp.array(X.todense()) #n_user * n_items의 행렬
P = jnp.array(np.random.normal(0, 0.001, size=(8190, 8190)))
P.at[jnp.diag_indices(Y.shape[0])].set(0) # constraint

def loss(X, P):
    Y = X @ P
    ret = (((X - Y) **2).sum() / X.shape[0])
    ret = ret + 0.01 * (P * P).sum() # regularization
    return ret
```

이 loss는 여러 방식으로 Optimize할 수 있지만, 여기서는 Stochastic Gradient Descent를 사용하겠습니다.

```python
lr = 0.05
for i in range(100):
    batch = np.random.choice(X.shape[0], 512)
    l = loss(jX[batch], P)
    print(l)
    r = grad(loss, argnums=1)(jX[batch], P)
    P -= lr * r
    P.at[jnp.diag_indices(P.shape[0])].set(0) # constraint
    lr *= 0.99 # weight decay
```

제약조건대로 유저가 봤던 아이템의 스코어를 낮춰 추천 대상에서 제외해 주는 부분을 추가합니다.

```python
scores = np.array(X @ Y)
scores = np.asarray((scores - X.astype(bool).astype(int) * 10000))
top_reco = (-scores).argsort(-1)[:, :100]
```

내부 데이터로 이 학습/테스트를 수행하는 부분은 [`2-1. Shallow AutoEncoder.ipynb`](2-1.%20Shallow%20AutoEncoder.ipynb)에 저장되어 있습니다.  
Stochastic Gradient Descent가 아닌, Exact solver를 이용한 풀이는 [`2-2. EASE^R.ipynb`](2-2.%20EASE%5ER.ipynb)에 저장되어 있습니다.  
문제가 요구하는 대로 입출력이 구현되어 수행되는 코드는 [`code_using_ease`](code_using_ease/) 디렉토리에 저장되어 있습니다.

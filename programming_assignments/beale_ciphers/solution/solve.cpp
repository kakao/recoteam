#include <stdio.h>
#include <stdlib.h>
#include <time.h>

const int K = 102;
const int N = 302;
const int M = 302;

int X[K][K], Y[K][K], Q[N][M], _C[K][K];
int v[K], t[K], q[K];


bool freivald(int X[][K], int Y[][K], int Q[][M], int x, int y, int n, int m, int k){
    int T = 10;
    while(T--){
        for(int i=0; i<k; i++)
            v[i] = rand() % 2;

        for(int i=0; i<k; i++){
            t[i] = q[i] = 0;
            for(int j=0; j<k; j++){
                t[i] += Q[x+i][y+j] * v[j];
                q[i] += Y[i][j] * v[j];
            }
        }
        for(int i=0; i<k; i++){
            v[i] = 0;
            for(int j=0; j<k; j++)
                v[i] += X[i][j] * t[j];
        }
        for(int i=0; i<k; i++)
            if(v[i] != q[i])
                return 0;
    }
    return 1;
}


bool back(int X[][K], int Y[][K], int Q[][M], int x, int y, int n, int m ,int k){

    for(int i=0; i<k; i++)
        for(int j=0; j<k; j++)
           _C[i][j] = 0;

    for(int i=0; i<k; i++)
        for(int j=0; j<k; j++)
            for(int r=0; r<k; r++)
                _C[i][j] += X[i][r] * Q[x+r][y+j];

    for(int i=0; i<k; i++)
        for(int j=0; j<k; j++)
            if(_C[i][j] != Y[i][j])
                return 0;
    return 1;
}


void solve(){
    int n, m, k;
    scanf("%d %d %d", &n, &m, &k);
    for(int i=0; i<k; i++)
        for(int j=0; j<k; j++)
            scanf("%d", &X[i][j]);
    for(int i=0; i<k; i++)
        for(int j=0; j<k; j++)
            scanf("%d", &Y[i][j]);

    for(int i=0; i<n; i++)
        for(int j=0; j<m; j++)
            scanf("%d", &Q[i][j]);

    int ans = 0;
    for(int i=0; i<n-k+1; i++)
        for(int j=0; j<m-k+1; j++)
            if(freivald(X, Y, Q, i, j, n, m, k))
                ++ans;

    printf("%d\n", ans);
}


int main(){
    srand(time(NULL));
    int T;
    scanf("%d", &T);
    while( T-- ) solve();
}

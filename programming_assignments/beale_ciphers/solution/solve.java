import java.util.*;

public class Main{
    public static void main(String args[]){
        Task solver = new Task();
        solver.solve();
    }
}

class Task{
    public void solve(){
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();

        for(int R=1; R<=T; R++)
            Do(sc);
    }

    public boolean freivald(int X[][], int Y[][], int Q[][], int x, int y, int n, int m, int k){
        int T = 10;
        int v[] = new int[k];
        int t[] = new int[k];
        int q[] = new int[k];
        Random rd = new Random();

        while( T-- > 0 ) {
            for(int i=0; i<k; i++)
                v[i] = rd.nextInt(2);

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
                if( v[i] != q[i] ) return false;

        }
        return true;
    }

    public void Do(Scanner sc){
        int n, m, k;
        n = sc.nextInt();
        m = sc.nextInt();
        k = sc.nextInt();

        int X[][] = new int[k][k];
        int Y[][] = new int[k][k];
        int Q[][] = new int[n][m];

        for(int i=0; i<k; i++)
            for(int j=0; j<k; j++)
                X[i][j] = sc.nextInt();

        for(int i=0; i<k; i++)
            for(int j=0; j<k; j++)
                Y[i][j] = sc.nextInt();

        for(int i=0; i<n; i++)
            for(int j=0; j<m; j++)
                Q[i][j] = sc.nextInt();

        int ans = 0;
        for(int i=0; i<n-k+1; i++)
            for(int j=0; j<m-k+1; j++)
                if(freivald( X, Y, Q, i, j, n, m, k ))
                    ++ans;

        System.out.println(ans);
    }
}

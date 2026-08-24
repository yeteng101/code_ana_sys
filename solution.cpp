#include <iostream>
#include <algorithm>
using namespace std;

const int MAXN = 32;

int n;
long long w[MAXN][MAXN];
int color[MAXN];
long long best = 0;

// Assign vertex u to one of the two groups and accumulate the
// total weight of edges that cross the current cut.
void dfs(int u, long long current) {
    if (u == n) {
        best = max(best, current);
        return;
    }

    // Put u in group 0: it crosses every earlier vertex in group 1.
    long long add0 = 0;
    for (int v = 0; v < u; ++v) {
        if (color[v] == 1) {
            add0 += w[u][v];
        }
    }
    color[u] = 0;
    dfs(u + 1, current + add0);

    // Put u in group 1: it crosses every earlier vertex in group 0.
    long long add1 = 0;
    for (int v = 0; v < u; ++v) {
        if (color[v] == 0) {
            add1 += w[u][v];
        }
    }
    color[u] = 1;
    dfs(u + 1, current + add1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> w[i][j];
        }
    }

    dfs(0, 0);
    cout << best << '\n';

    return 0;
}

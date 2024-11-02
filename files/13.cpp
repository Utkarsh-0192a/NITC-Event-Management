#include <bits/stdc++.h>
using namespace std;

#ifndef ONLINE_JUDGE
#define debug(x) cerr<<#x<<" "; _print(x); cerr<<'\n';
#else
#define debug(x)
#endif

#define fastio() ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL)
#define pb push_back
#define all(x) x.begin(),x.end()

typedef long long ll;
typedef unsigned long long ull;

void _print(ll t){cerr<<t;}
void _print(int t){cerr<<t;}
void _print(string t){cerr<<t;}
void _print(char t){cerr<<t;}
void _print(float t){cerr<<t;}
void _print(double t){cerr<<t;}
void _print(ull t){cerr<<t;}
template<class T> void _print(vector<T> v){cerr<<"[ ";for(T i: v){_print(i);cerr<<" ";}cerr<<"]";}
template<class T> void _print(set<T> v){cerr<<"[ ";for(T i: v){_print(i);cerr<<" ";}cerr<<"]";}
template<class T> void _print(multiset<T> v){cerr<<"[ ";for(T i: v){_print(i);cerr<<" ";}cerr<<"]";}
template<class T, class V> void _print(map<T, V> v){cerr<<"[ ";for(auto i : v){_print(i);cerr<<" ";}cerr<<"]";}


int MOD = 1000000007;
void solve();

int main(){
	#ifndef ONLINE_JUDGE
	freopen("error.txt", "w", stderr);
	#endif
	
	fastio();

	int t=1;
	cin>>t;
	while (t--){solve(); cout<<"\n";}

return 0;}

void solve(){
	int n; cin>>n;
	//start
}
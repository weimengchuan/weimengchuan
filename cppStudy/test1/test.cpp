#include <iostream>
using namespace std;

int main()
{
	auto f = [](int a) -> int { return a + 1; };
	cout << f(1) << endl;
	return 0;
}


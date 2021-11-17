#include <time.h>   // clock_t, clock, CLOCKS_PER_SEC
#include <random>   // mt19937 and uniform_int_distribution
#include <iostream> // cout
#include <string>   // string
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

using namespace std;

// Generate sorted n size array with uniform increment
void generateSortIntArr(int* arr, const int size, const int min, const int max)
{
    for (int i = 0; i < size; i++)
        arr[i] = i;
}

double sec(void)
{
    return double(clock()) / double(CLOCKS_PER_SEC);
}


// iterative lambda to return arr[i], where arr[i] = x
// :param: int arr[], int size, int x
int bs_it(int arr[], const int size, const int x)
{
    int mid, low = 0, high = size - 1;
    while (low <= high)
    {
        mid = (low + high) / 2;
        if (arr[mid] == x)
            return arr[mid];
        else if (arr[mid] > x)
            high = mid - 1;
        else
            low = mid + 1;
    }
    return -1;
}

// recursive lambda to return int where arr[i] = x
// :param: int arr[], int size, int x
int bs_re(int arr[], const int size, const int x)
{
    // inner recursive lambda
    auto bs_re_imp = [](int arr[], const int low, const int high, const int x, auto& bs_ref) mutable -> int
    {
        int mid = (low + high) / 2;
        if (low > high)
            return -1;
        else if (arr[mid] == x)
            return arr[mid];
        else if (arr[mid] > x)
            return bs_ref(arr, low, mid - 1, x, bs_ref);
        else
            return bs_ref(arr, mid + 1, high, x, bs_ref);
    };
    return bs_re_imp(arr, 0, size, x, bs_re_imp);
}

int main()
{
    // setting up parameters
    const double K = 1000;
    const int n = 100000;
    int arr[n];
    generateSortIntArr(arr, n, 0, n);

    // Iterative version
    double T1 = sec();
    for (int j = 0; j < K; j++)
        for (int i = 0; i < n; i++)
            if (bs_it(arr, n, i) != i)
                cout << "\nERROR: ";
    double T2 = sec();
    cout << "Total iterative run time = " << T2 - T1 << " seconds\n";
    cout << "Individual iterative version run time = " << (((T2 - T1) / n) * 1.E9) / K << " nanosec\n\n";

    // Recursive version
    T1 = sec();
    for (int j = 0; j < K; j++)
        for (int i = 0; i < n; i++)
            if (bs_re(arr, n, i) != i)
                cout << "\nERROR";
    T2 = sec();
    cout << "Total recursive run time = " << T2 - T1 << " seconds\n";
    cout << "Individual recursive version run time = " << (((T2 - T1) / n) * 1.E9) / K << " nanosec\n\n";

    // infinite loop to prevent program from closing before checking benchmark
    cout << "On infinite loop to prevent software closing before recording benchmark.\n";
    while (1)
    {
        cout << "Sleeping" << endl;
        Sleep(10000);
    }
    return 0;
}
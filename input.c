// An Example C file to use for testing 

#include <stdio.h>

#define MAX 100

int add(int *a, int *b) {
    return *a + *b;
}

int main() {
    int a = 3;
    int b = 4;
    a++;
    
    int c = add(&a, &b);
    printf("c = %d\n", c);
    printf("a + b = %d\n", a + b);

    if (a > b) {
        printf("a > b\n");
    } else {
        printf("a <= b\n");
    }

    return 0;
}
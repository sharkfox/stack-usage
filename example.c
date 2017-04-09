
int bar()
{
    int x = 4;
    return x;
}

int foo()
{
    int a[32];
    return bar();
}

int main(void)
{
    return foo();
}

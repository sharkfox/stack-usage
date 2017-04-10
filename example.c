
int bar()
{
    int x = 4;
    return x;
}

int foo()
{
    int a[32];
    return foo() + bar() + a[0];
}

int foobar()
{
    return foo() + bar();
}

int main(void)
{
    return foo();
}

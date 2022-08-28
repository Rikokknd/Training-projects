def fib(pos, now= 0, next= 1, counter= 0):
    if pos == counter:
        return now
    else:
        return fib(pos, now=next, next= now+next, counter= counter + 1)

if __name__ == "__main__":
    print(fib(100))
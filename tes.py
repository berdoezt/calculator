def calculate(s):
        """
        Time    O(n)
        Space   O(n)
        80 ms, faster than 22.22%
        """
        arr = []
        for c in s:
            arr.append(c)
        return helper(arr)

def helper(s):
    if len(s) == 0:
        return 0
    stack = []
    sign = '+'
    num = 0
    while len(s) > 0:
        c = s.pop(0)
        if c.isdigit():
            num = num*10+int(c)
        if c == '(':
            # do recursion to calculate the sum within the next (...)
            num = helper(s)
        if len(s) == 0 or (c == '+' or c == '-' or c == '*' or c == '/' or c == ')'):
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack[-1] = stack[-1]*num
            elif sign == '/':
                stack[-1] = int(stack[-1]/float(num))
            sign = c
            num = 0
            if sign == ')':
                break
    return sum(stack)

exp = raw_input()
print calculate(exp)
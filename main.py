import math

operator = "+-*/"

def add(s1, s2):
    result = ""

    if len(s1) > len(s2):
        s1,s2 = s2,s1
    
    
    diff = len(s2) - len(s1)
    carry = 0

    for i in range(len(s1) - 1, -1, -1):
        temp = int(s1[i]) + int(s2[i + diff]) + carry
        result += str(temp % 10)
        carry = temp // 10
        
    for i in range(len(s2) - len(s1) - 1, -1, -1):
        temp = int(s2[i]) + carry
        result += str(temp % 10)
        carry = temp // 10
    
    if carry:
        result += str(carry)

    return result[::-1]

def isSmaller(s1, s2):
    if len(s1) > len(s2):
        return False
    elif len(s1) < len(s2):
        return True
    
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False
        elif s1[i] < s2[i]:
            return True
    
    return False

def sub(s1, s2):
    result = ""

    sign = ""

    if isSmaller(s1, s2):
        s1,s2 = s2,s1
        sign = "-"

    diff = len(s1) - len(s2)
    carry = 0

    for i in range(len(s2) - 1, -1, -1):
        temp = int(s1[i + diff]) - int(s2[i]) - carry
        if temp < 0:
            temp += 10
            carry = 1
        else:
            carry = 0

        result += str(temp)
    
    # print result
        
    for i in range(len(s1) - len(s2) - 1, -1, -1):
        if s1[i] == '0' and carry:
            result += '9'
            continue
        
        temp = int(s1[i]) - carry
        if temp > 0 or i > 0:
            result += str(temp)
        
        carry = 0

    result = result[::-1].lstrip('0')
    if result == "":
        result = '0'

    return sign + result

def mul(s1, s2):
    if len(s1) == 0 or len(s2) == 0:
        return 0
    
    result = [0] * (len(s1) + len(s2)) # maximum possible digits
    i_1 = 0

    for i in range(len(s1) - 1, -1, -1):
        carry = 0
        i_2 = 0
        num_1 = int(s1[i])

        for j in range(len(s2) - 1, -1, -1):
            num_2 = int(s2[j])
            temp = num_1 * num_2 + result[i_1 + i_2] + carry
            carry = temp // 10
            result[i_1 + i_2] = temp % 10

            i_2 += 1
        
        if carry:
            result[i_1 + i_2] += carry
        
        i_1 += 1
    
    i = len(result) - 1
    while i >= 0 and result[i] == 0:
        i -= 1
    
    if i == -1:
        return "0"
    
    r = ""
    while i >= 0:
        r += str(result[i])
        i -= 1
    
    return r

def div(s1, s2):
    result = ""

    i = 0
    temp_1 = int(s1[i])
    divisor = int(s2)
    while temp_1 < divisor:
        if i == len(s1) -1:
            break

        temp_1 = temp_1 * 10 + int(s1[i + 1])
        i += 1
    
    i += 1

    while len(s1) > i:
        result += str(int(math.floor(temp_1 // divisor)))
        temp_1 = (temp_1 % divisor) * 10 + int(s1[i])
        i += 1
    
    result += str(int(math.floor(temp_1 // divisor)))

    if len(result) == 0:
        return "0"
        
    return result

def total(st):
    result = st[0]

    for i in st[1:]:
        if i[0] == "-" and result[0] == "-":
            result = "-" + add(result[1:], i[1:])
        elif i[0] == "-":
            result = sub(result, i[1:])
        elif result[0] == "-":
            result = sub(i, result[1:])
        else:
            result = add(result, i)

    return result

def calculate(exp):
    if len(exp) == 0:
        return 0
    
    stack = []
    sign = '+'
    result = ""

    while len(exp) > 0:
        ch = exp.pop(0)
        
        if ch.isdigit():
            result += ch # to accomodate number > 1 digit
        
        if ch == '(':
            result = calculate(exp) # prioriteze to calculate inside parenthesis

        if len(exp) == 0 or ch in operator or ch == ')':
            if sign == '+':
                stack.append(result)
            elif sign == '-':
                if result[0] == "-":
                    stack.append(result[1:])
                else:
                    stack.append("-"+result)
            elif sign == '*':
                if stack[-1][0] == '-' and result[0] == "-":
                    stack[-1] = mul(stack[-1][1:], result[1:])
                elif stack[-1][0] == "-":
                    stack[-1] = "-" + mul(stack[-1][1:], result)
                elif result[0] == "-":
                    stack[-1] = "-" + mul(stack[-1], result[1:])
                else:
                    stack[-1] = mul(stack[-1], result)

            elif sign == '/':
                if stack[-1][0] == '-' and result[0] == "-":
                    stack[-1] = div(stack[-1][1:], result[1:])
                elif stack[-1][0] == "-":
                    stack[-1] = "-" + div(stack[-1][1:], result)
                elif result[0] == "-":
                    stack[-1] = "-" + div(stack[-1], result[1:])
                else:
                    stack[-1] = div(stack[-1], result)
            
            sign = ch
            result = ""

            if ch == ')':
                break # return immediately to denotes blocks (....) done calculated

    return total(stack)

if __name__ == "__main__":
    exp = list(raw_input())
    print(calculate(exp))
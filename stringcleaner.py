import re
def strinsert(oldstr, index, newchar):
    return oldstr[:index] + newchar + oldstr[index+1:]

def clean(string):
    string = string.replace("\\-", "")
    string = string.replace("**", "^")
    sqrts = [m.span() for m in re.finditer("sqrt", string)]
    for sqrt in sqrts:
        string = strinsert(string, sqrt[0], "S")
        string = strinsert(string, sqrt[1], "[")
        lefts = 0
        for i in range(sqrt[1]+1, len(string)):
            if string[i] == '(':
                lefts += 1
            elif string[i] == ')':
                if lefts > 0:
                    lefts -= 1
                else:
                    string = strinsert(string, i, "]")
                    break
    return string


test = "c\-0\-0 + 2**(1/5)*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2) + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2) + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2) + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)"
print(clean(test))

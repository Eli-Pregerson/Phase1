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


str1 = "c\-0\-0 + c\-1\-0 + c\-2\-0 + c\-3\-0 + c\-4\-0 + c\-5\-0"
str2 = "c\-0\-0 + 2**(1/5)*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2) + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2) + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2) + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)"
str3 = "c\-0\-0 + 2**(2/5)*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**2 + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**2 + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**2 + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**2"
str4 = "c\-0\-0 + 2**(3/5)*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**3 + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**3 + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**3 + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**3"
str5= "c\-0\-0 + 2**(4/5)*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**4 + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**4 + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**4 + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**4 - 1"
str6 = "c\-0\-0 + 2*c\-1\-0 + c\-2\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 - 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**5 + c\-3\-0/(-2**(4/5)*sqrt(5)/8 - 2**(4/5)/8 + 2**(4/5)*I*sqrt(5/8 - sqrt(5)/8)/2)**5 + c\-4\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 - 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**5 + c\-5\-0/(-2**(4/5)/8 + 2**(4/5)*sqrt(5)/8 + 2**(4/5)*I*sqrt(sqrt(5)/8 + 5/8)/2)**5 - 1"

print(clean(str1))
print(clean(str2))
print(clean(str3))
print(clean(str4))
print(clean(str5))
print(clean(str6))

def replaceSpace(s):
    # write code here
    if s:
        p = len(s)
        for i in range(0, p):
            if s[i] == ' ':
                s = s + '  '
        q = len(s)
        while p != q:
            if s[p - 1] == ' ':
                s = s[:q - 3] + '%20' + s[q:]
                q -= 3
            else:
                s = s[:q - 1] + s[p - 1] + s[q:]
                q -= 1
            p -= 1
    return s

s = "hello world"
s = replaceSpace(s)
print(s)
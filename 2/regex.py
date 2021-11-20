def calculate(data, findall):
    reg = findall(r"([abc])([+-]?)=([abc])?([+-]?\d+)?")
    
    for a, sign, b, num in reg:
        right_number = data.get(b, 0) + int(num or 0)
        if sign == "-":
            data[a] -= right_number
        elif sign == "+":
            data[a] += right_number
        else:
            data[a] = right_number
    return data
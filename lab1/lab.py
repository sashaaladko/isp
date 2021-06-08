def exchange(usd_rate, money):
    result = round(money / usd_rate, 2)
    return result


result1 = exchange(60, 30000)
print(result1)
result2 = exchange(56, 30000)
print(result2)
result3 = exchange(65, 30000)
print(result3)
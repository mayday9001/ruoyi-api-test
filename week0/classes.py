class Calculator:
    def __init__(self, owner):
        print(f"[造对象] owner = {owner}")
        self.owner = owner       # 身上存一个 owner
        self.history = []        # 身上存一个空列表（用来记历史）

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")    # 存进自己的历史
        return result

    def show_history(self):
        print(f"{self.owner} 的计算历史：")
        for h in self.history:
            print("  ", h)


# 造对象
calc = Calculator("mayday")

# 用它
print(calc.add(1, 2))       # 3
print(calc.add(10, 20))     # 30

# 看历史
calc.show_history()

calc1 = Calculator("张三")
print(calc1.add(1, 2))
calc1.show_history()
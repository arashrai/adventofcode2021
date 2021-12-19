from __future__ import annotations

with open("/Users/arash/Downloads/day18.txt") as f:
    puzzle = f.readlines()


class SnailFishNum:
    def __init__(self, sfn, depth=0, parent=None):
        self.value = None
        self.depth = depth
        self.parent = parent
        self.sfn = sfn

        if sfn.isnumeric():
            self.value = int(sfn)
            self.left = None
            self.right = None
        else:
            i = self.find_middle()
            self.left = SnailFishNum(self.sfn[1:i], depth + 1, self)
            self.right = SnailFishNum(self.sfn[i + 1 : -1], depth + 1, self)

    def find_middle(self):
        commas = [i for i, x in enumerate(self.sfn) if x == ","]
        for i in commas:
            a = self.sfn[:i].count("[")
            b = self.sfn[:i].count("]")
            c = self.sfn[i + 1 :].count("[")
            d = self.sfn[i + 1 :].count("]")
            if a - b == 1 and d - c == 1:
                return i

    def get_sfn(self):
        if self.value is not None:
            return str(self.value)
        return "[" + self.left.get_sfn() + "," + self.right.get_sfn() + "]"

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def explode_left_most(self):
        if self.left.need_explode():
            self.left.explode_left_most()
        elif (
            self.depth >= 4
            and self.value is None
            and self.right.value is not None
            and self.left.value is not None
        ):
            self.explode()
        elif self.right.need_explode():
            self.right.explode_left_most()

    def split_left_most(self):
        if self.value is None and self.left.need_split():
            self.left.split_left_most()
        elif self.value is not None and self.value >= 10:
            self.split()
            if self.need_explode():
                self.explode()
        elif self.value is None and self.right.need_split():
            self.right.split_left_most()

    def explode(self):
        self.parent.send_left(self.left.value, self)
        self.parent.send_right(self.right.value, self)
        self.value = 0
        self.sfn = "0"
        self.left = None
        self.right = None

    def split(self):
        left_val = self.value // 2
        right_val = self.value - left_val
        self.value = None
        self.sfn = "[" + str(left_val) + "," + str(right_val) + "]"
        self.left = SnailFishNum(str(left_val), self.depth + 1, self)
        self.right = SnailFishNum(str(right_val), self.depth + 1, self)

    def send_right(self, v, sender):
        if self.value is not None:
            self.value += v
            self.sfn = str(self.value)
        elif self.right == sender:
            if self.parent:
                self.parent.send_right(v, self)
        elif self.parent == sender:
            self.right.send_right(v, self)
        elif self.right:
            self.right.send_left(v, self)

    def send_left(self, v, sender):
        if self.value is not None:
            self.value += v
            self.sfn = str(self.value)
        elif self.left == sender:
            if self.parent:
                self.parent.send_left(v, self)
        elif self.parent == sender:
            self.left.send_left(v, self)
        elif self.left:
            self.left.send_right(v, self)

    def print_root(self):
        if self.parent is None:
            print(self.get_sfn())
            print(self)
        else:
            self.parent.print_root()

    def need_split(self):
        if self.value is not None and self.value >= 10:
            return True
        elif self.value is not None:
            return False
        return self.left.need_split() or self.right.need_split()

    def need_explode(self):
        if self.depth >= 4 and self.value is None:
            return True
        elif self.value is not None:
            return False
        return self.left.need_explode() or self.right.need_explode()

    def __add__(self, sfn):
        source = "[" + self.get_sfn() + "," + sfn.get_sfn() + "]"
        res = SnailFishNum(source)

        while True:
            while res.need_explode():
                res.explode_left_most()

            if res.need_split():
                res.split_left_most()

            if not res.need_explode() and not res.need_split():
                break

        return res

    def __str__(self):
        ret = ""

        if self.left:
            ret += self.left.__str__()

        if self.value is not None:
            ret = "\t" * self.depth + repr(self.value) + "\n"
        else:
            ret += "\t" * self.depth + "*" + str(self.depth) + "*" + "\n"

        if self.right:
            ret += self.right.__str__()

        return ret


snail_fish_nums = []

for p in puzzle:
    value = p.strip()
    snail_fish_nums.append(SnailFishNum(value))

res = snail_fish_nums[0]
for x in snail_fish_nums[1:]:
    res += x
    print(res.get_sfn())
    print(res)
    print(res.magnitude())

curr_max = 0
for i, x in enumerate(snail_fish_nums):
    for j, y in enumerate(snail_fish_nums):
        if i != j:
            res = x + y
            print(res.get_sfn(), res.magnitude())
            print(res)
            curr_max = max(curr_max, res.magnitude())

print(curr_max)

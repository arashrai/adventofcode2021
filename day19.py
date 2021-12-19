from __future__ import annotations

from collections import Counter, defaultdict, deque
from functools import lru_cache
from math import ceil, floor

with open("/Users/arash/Downloads/day19.txt") as f:
    puzzle = f.readlines()

# puzzle = """--- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401

# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390

# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562

# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596

# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14""".split(
#     "\n"
# )


v_list = []
v_map = {}
v_set = set()

curr_scanner = -1

for p in puzzle:
    if "scanner" in p:
        curr_scanner += 1
        v_map[curr_scanner] = set()
        continue

    elif p == "\n" or p == "":
        continue

    v_map[curr_scanner].add(tuple(int(n) for n in p.strip().split(",")))


def get_all_point_perms(x, y, z):
    poss = set()

    for a in (1, -1):
        for b in (1, -1):
            for c in (1, -1):
                poss.add((x * a, y * b, z * c))

    new_poss = set()
    for a, b, c in poss:
        new_poss.add((a, b, c))
        new_poss.add((a, c, b))
        new_poss.add((b, a, c))
        new_poss.add((b, c, a))
        new_poss.add((c, a, b))
        new_poss.add((c, b, a))

    return new_poss


def orient(x_pos, y_pos, z_pos, rot, x, y, z):
    if not x_pos:
        x *= -1
    if not y_pos:
        y *= -1
    if not z_pos:
        z *= -1

    if rot == 1:
        return x, y, z
    elif rot == 2:
        return x, z, y
    elif rot == 3:
        return y, x, z
    elif rot == 4:
        return y, z, x
    elif rot == 5:
        return z, x, y
    elif rot == 6:
        return z, y, x


def find_overlap(s1, s2):
    for a, b, c in v_map[s1]:
        for x, y, z in v_map[s2]:
            for x_pos in (True, False):
                for y_pos in (True, False):
                    for z_pos in (True, False):
                        for rot in (1, 2, 3, 4, 5, 6):
                            x_final, y_final, z_final = orient(x_pos, y_pos, z_pos, rot, x, y, z)
                            rel_x = a - x_final
                            rel_y = b - y_final
                            rel_z = c - z_final

                            relative_changed_points = set()
                            for i, j, k in v_map[s2]:
                                i_final, j_final, k_final = orient(
                                    x_pos, y_pos, z_pos, rot, i, j, k
                                )
                                relative_changed_points.add(
                                    (i_final + rel_x, j_final + rel_y, k_final + rel_z)
                                )

                            intersect = relative_changed_points.intersection(v_map[s1])
                            if len(intersect) == 12:
                                correctly_oriented_points = set()
                                for i, j, k in v_map[s2]:
                                    i_final, j_final, k_final = orient(
                                        x_pos, y_pos, z_pos, rot, i, j, k
                                    )
                                    correctly_oriented_points.add((i_final, j_final, k_final))
                                v_map[s2] = correctly_oriented_points
                                return rel_x, rel_y, rel_z


diff_map = {}
diff_map[0] = (0, 0, 0)

scanners = [k for k in v_map.keys()]
scanners.remove(0)

found = [0]

while len(scanners):
    for s in scanners:
        for f in found:
            res = find_overlap(f, s)
            if res is not None:
                x, y, z = res
                if f == 0:
                    diff_map[s] = (x, y, z)
                else:
                    diff_map[s] = (x + diff_map[f][0], y + diff_map[f][1], z + diff_map[f][2])
                if s in scanners:
                    scanners.remove(s)
                    print(len(scanners), "scanners left!")
                if s not in found:
                    found.append(s)

for k, v in diff_map.items():
    print(k, v)

all_beacons = set()

for k, v in v_map.items():
    for x, y, z in v:
        all_beacons.add((x + diff_map[k][0], y + diff_map[k][1], z + diff_map[k][2]))

print("part 1", len(all_beacons))

max_man = 0

for i in diff_map:
    for j in diff_map:
        if i != j:
            man = (
                abs(diff_map[i][0] - diff_map[j][0])
                + abs(diff_map[i][1] - diff_map[j][1])
                + abs(diff_map[i][2] - diff_map[j][2])
            )
            max_man = max(max_man, man)

print("part 2", max_man)
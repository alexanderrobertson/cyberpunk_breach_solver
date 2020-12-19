from solver import Puzzle


g1 = '1115be5b15bb5ee1e5eebb51e'
t1 = 'be 51 155'

g2 = '11beb1b11ebb15b51e155ee51'
t2 = '5b 15 5e1'

g3 = '115555115511b5ee11b1b551e'
t3 = '15b 5ee 5155'

g4 = '1e15b1e151515eb1551bbb5b1'
t4 = '151 1b b1b'





for g, t in [(g1, t1), (g2, t2), (g3, t3), (g4, t4)]:
    puzzle = Puzzle(g, t, buffer_size=8)

    print(puzzle)

    try:
        print(puzzle.solution['score'])
    except:
        print('No score')

    print('='*50)
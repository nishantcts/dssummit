import os, sys, time
import termcolor
import random


class Genetic_Queen:
    def __init__(self, verbose=False, show_board=False, show_score=False):
        self.show_score = show_score
    def populate(self, combination_list):
        blocked_moves, moves_possible, coins_pos = [], [], []
        hit_moves = {}
        [[moves_possible.append((row, col)) for col in range(1, 9)] for row in range(1, 9)]
        for i in range(8):
            if combination_list[i] != 0:
                coins_pos.append((combination_list[i], i + 1))

        for queen_pos in coins_pos:
            coin_blocked = []
            for i in range(1, 9):
                blocked_moves.append((queen_pos[0], i))
                blocked_moves.append((i, queen_pos[1]))
                coin_blocked.append((queen_pos[0], i))
                coin_blocked.append((i, queen_pos[1]))
                if queen_pos[0] + i < 9 and queen_pos[1] + i < 9:
                    blocked_moves.append((queen_pos[0] + i, queen_pos[1] + i))
                    coin_blocked.append((queen_pos[0] + i, queen_pos[1] + i))
                if queen_pos[0] - i > 0 and queen_pos[1] - i > 0:
                    blocked_moves.append((queen_pos[0] - i, queen_pos[1] - i))
                    coin_blocked.append((queen_pos[0] - i, queen_pos[1] - i))
                if queen_pos[0] + i < 9 and queen_pos[1] - i > 0:
                    blocked_moves.append((queen_pos[0] + i, queen_pos[1] - i))
                    coin_blocked.append((queen_pos[0] + i, queen_pos[1] - i))
                if queen_pos[0] - i > 0 and queen_pos[1] + i < 9:
                    blocked_moves.append((queen_pos[0] - i, queen_pos[1] + i))
                    coin_blocked.append((queen_pos[0] - i, queen_pos[1] + i))

            blocked_moves = list(dict.fromkeys(blocked_moves))
            hit_moves[queen_pos[0] * 10 + queen_pos[1]] = coin_blocked
        [moves_possible.remove(move) for move in blocked_moves if move in moves_possible]

        hits = self.score_population(coins_pos, hit_moves)
        return (hits, combination_list)

    def score_population(self, coins_pos, hit_moves):
        hits = 0
        for n, coin in enumerate(coins_pos):
            if n is not 0:
                for key in hit_moves.keys():
                    if coin[0] * 10 + coin[1] != key and key % 10 < coin[1]:
                        if coin in hit_moves[key]:
                            hits = hits + 1

        return hits

    def generateChromozomes(self, parents):
        hits1, parent1 = parents[0]
        hits2, parent2 = parents[1]
        for i in range(1, 8):
            if abs(parent1[i - 1] - parent1[i]) < 2:
                temp = parent1[i]
                parent1[i] = parent2[i]
                parent2[i] = temp

            if abs(parent2[i - 1] - parent2[i]) < 2:
                temp = parent1[i]
                parent1[i] = parent2[i]
                parent2[i] = temp

        new_parent1 = self.populate(parent1)
        new_parent2 = self.populate(parent2)

        if new_parent1[0] > hits1:
            new_parent1 = parents[0]
        if new_parent2[0] > hits2:
            new_parent2 = parents[1]

        return (new_parent1, new_parent2)

    def Mutation(self, children):
        ret_children = []
        for element in children:
            child = element[1]
            if len(child) != len(list(dict.fromkeys(child))):
                replacement = []
                [replacement.append(val) for val in range(1, 9) if val not in child]
                for n in range(len(child)):
                    for k in range(len(child)):
                        if n != k and child[n] == child[k]:
                            child[n] = replacement.pop(0)
            half = len(child) // 2
            right = random.randrange(half, len(child))
            left = random.randrange(1, half)
            child[left], child[right] = child[right], child[left]
            child = self.populate(child)
            if child[0] > element[0]:
                child = element
            ret_children.append(child)
        return ret_children

    def generateGen1(self):
        gen1_parents = []
        for _ in range(100):
            gen1_parents.append([random.randrange(1, 9) for i in range(1, 9)])
        gen1 = []

        for parents in gen1_parents:
            if parents not in gen1:
                gen1.append(parents)
        return gen1

    def select_Parents(self, children):
        hit_list = []
        new_parent1, new_parent2 = 0, 0
        lowest_hits = 100
        for vals in children:
            hits, vals = self.populate(vals)
            if hits not in hit_list:
                hit_list.append(hits)
            if hits <= lowest_hits:
                lowest_hits = hits
                new_parent2 = new_parent1
                new_parent1 = (hits, vals)
        return (new_parent1, new_parent2)

    def check_won(self, combinations):
        for val in combinations:
            if val[0] == 0:
                return ("Won", val)
        return "Continue"

    def start(self):
        Run = True
        gen1_parents = self.generateGen1()
        selected_parents = self.select_Parents(gen1_parents)

        while Run:
            status = self.check_won(selected_parents)
            if status[0] == "Won":
                answer = status[1]
                Run = False
                break

            children = self.generateChromozomes(selected_parents)
            status = self.check_won(children)
            if status[0] == "Won":
                answer = status[1]
                Run = False
                break

            children = self.Mutation(children)
            status = self.check_won(children)
            if status[0] == "Won":
                answer = status[1]
                Run = False
                break
            selected_parents = children
            print("scores", children[0][0], children[1][0])
        answer = answer[1]
        new_answer = ''
        for val in answer:
            val = val - 1
            new_answer = new_answer + " " + str(val)
        self.result = new_answer[1:]


if __name__ == "__main__":
    queen8 = Genetic_Queen()
    queen8.start()
    print(queen8.result)

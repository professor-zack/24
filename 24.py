import random
from itertools import permutations
import time

deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
str_deck = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
mod_str_deck = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def draw_cards():
    cards = random.choices(str_deck, k=4)
    return cards

def permuter(cards):
    unique_permutations = set(permutations(cards))
    unique_permutations = [list(perm) for perm in unique_permutations]
    return unique_permutations

def opper(op, cards, current):
    exps = []
    exp = ""
    exp += str(cards[0])
    if len(cards)==1:
        current += exp
        return [current]
    exp += op
    current += exp
    exps += opper("*", cards[1:], current)
    exps += opper("/", cards[1:], current)
    exps += opper("+", cards[1:], current)
    exps += opper("-", cards[1:], current)
    return exps

def bracket_inserter(exp):
    copy = exp[:]
    if exp[0]=='-':
        copy = copy[1:]
    output = []
    boom = []
    one_brac = [(0,2), (0,4), (0,6), (2,4), (2,6), (4,6)]
    two_brac = [[(0,2), (0,4)], [(0,2), (0,6)], [(0,2), (4,6)], [(0,4),(0,6)], [(0,4), (2,4)], [(0,4), (2,6)], [(0,6), (2,4)], [(0,6), (2,6)], [(0,6), (4,6)], [(2,4), (2,6)], [(2,6), (4,6)]]
    for ele in one_brac:
        first = copy[:ele[0]]+'('+copy[ele[0]:]
        second = first[:ele[1]+2]+')'+first[ele[1]+2:]
        second = second.replace('0', '10')
        output.append(second)
    for ele in two_brac:
        bro = two_brac_inserter(copy, ele[0], ele[1])
        output.append(bro)
    for idx,ele in enumerate(output):
        nom = ele.replace('0', '10')
        if exp[0]=='-':
            output[idx] = '-'+ nom
        else:
            output[idx]=nom
    return output

def two_brac_inserter(exp, first, second):
    a = first[0]
    b = first[1]
    c = second[0]
    d = second[1]
    alpha = exp[:a]+'('+exp[a:]
    bravo = alpha[:b+2]+')'+alpha[b+2:]
    if c<b:
        charlie = bravo[:c+1]+'('+bravo[c+1:]
    elif c>b:
        charlie = bravo[:c+2]+'('+bravo[c+2:]
    if d<b:
        delta = charlie[:d+3]+')'+charlie[d+3:]
    else:
        delta = charlie[:d+4]+')'+charlie[d+4:]
    return delta

def evaluator(final):
    correct = []
    for exp in final:
        try:
            result = eval(exp)
        except ZeroDivisionError:
            continue
        if result==24:
            #correct.append(exp)
            print(exp)
            return
    # if len(correct)==0:
    #     print("There are no solutions from these 4 cards to get 24")
    #     return False
    # else:
    #     print(f"There are {len(correct)} unique solutions from these 4 cards to get 24")
    #     print(correct)
    #     return True
    print("There are no solutions from these 4 cards to get 24")
    return

def main():
    #cards = draw_cards()
    #print(cards[0], cards[1], cards[2], cards[3])
    cards = ['2', '3', '7', '5']
    start = time.time()
    if sum([int(x) for x in cards])==24:
        print("The sum of these cards add up to 24")
        return
    modded_cards = ['0' if x=='10' else x for x in cards]
    card_permutes = permuter(modded_cards)
    processed = []
    for card_perm in card_permutes:
        ax = opper("+", card_perm, "")
        bx = opper("-", card_perm, "")
        cx = opper("*", card_perm, "")
        dx = opper("/", card_perm, "")
        card_groupings = ax+bx+cx+dx
        card_groupings = list(set(card_groupings))
        processed += card_groupings
    # neg = processed[:]
    # for idx,ele in enumerate(neg):
    #     neg[idx] = '-'+ele
    # processed += neg
    final = []
    for ele in processed:
        final+=bracket_inserter(ele)
    final = list(set(final))
    print(len(final))
    sol_status = evaluator(final)
    end=time.time()
    print(f"{end-start} seconds elapsed")
    return
    

"""
Changes to make:

1.Keep track of the exact groupings/operations from start to end that results in successfully obtaining 24
2. Verify if there is a need to add a negative sign to the front of all duplicated initial expressions
3. After inserting brackets, way too many expressions are obtained in 'final' Need to cut this down drastically

Failure case #1: [6, 10, 6, 7] can get 24 by (10-7)*6+6=24. FIXED
Failure case #2: [5, 5, 4, 9] can get 24 by (9-5)*5+4=24. FIXED
Failure case #3: [10, 3, 10, 9] can get 24 by 3*(9-10/10) FIXED
Failure case #4: [1, 5, 7, 4] can get 24 by 7*4-5+1=24. FIXED
Failure case #5: [2, 3, 7, 5] can get 24 by 7*3+5-2=24. FIXED

There may be more failure cases that have not yet been found, but the above 5 are just the ones discovered through some brief testing of the very first complete initial version.
These 5 failures are likely very representative of most (if not all) failure cases. All have been solved.
"""
    
if __name__ == '__main__':
    main()
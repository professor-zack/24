import random
from itertools import permutations

deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10]

def draw_cards():
    cards = random.sample(deck, 4)
    return cards

def permuter(cards):
    unique_permutations = set(permutations(cards))
    unique_permutations = [list(perm) for perm in unique_permutations]
    return unique_permutations

def grouping(op, cards, current):
    """
    ['1, 2, 3+4' : [1, 2, 7]]
    """
    groupings = []
    exp = ""
    exp += op
    exp += str(cards[0])
    current += exp
    if len(cards)==1:
        return [current]
    groupings += grouping("+", cards[1:], current)
    groupings += grouping("-", cards[1:], current)
    groupings += grouping("f", cards[1:], current)
    return groupings

"""
The idea behind the above groupings function is that between numbers, either a +, - or f is placed. A "f" would
just be used to replace in a comma later to separate the different groupings of numbers. For example, "+3+4f5-2" would
get subsequently processed to become "+3+4, 5-2" ---> "7, 3"
"""

def grouping_formatter(groupings):
    for idx,group in enumerate(groupings):
        new_group = group.replace('f', ',')
        if new_group[0]=='+' or new_group[0]==',':
            new_group = new_group[1:]
        groupings[idx] = new_group
    
    return list(set(groupings))

def grouping_eval(groupings):
    final = []
    for group in groupings:
        sub_groups = group.split(',')
        evaluated = []
        for sub_group in sub_groups:
            evaluated.append(eval(sub_group))
        # evaluated = list(set(evaluated))
        # evaluated = sorted(evaluated)
        if evaluated in final:
            continue
        else:
            final.append(evaluated)
    return final

def early_24_checker(groupings):
    filtered = [x for x in groupings if sum(x)==24]
    if len(filtered)>0:
        return True, filtered
    else:
        return False, []

def list_to_tuple(lst):
    return tuple(sorted(lst))

def duplicate_filtering(processed_card_groups):
    unique_card_groups = {}
    for card_group in processed_card_groups:
        key = list_to_tuple(card_group)
        if key not in unique_card_groups:
            unique_card_groups[key] = card_group
    
    unique_processed_card_groups = list(unique_card_groups.values())
    return unique_processed_card_groups

def odd_negative_filtering(unique_processed):
    output = []
    for group in unique_processed:
        negative_count = 0
        for num in group:
            if num < 0:
                negative_count+=1
        if negative_count%2 == 0:
            output.append(group)
    return output

def single_num_filtering(more_processed):
    return [group for group in more_processed if len(group)>1]

def final_grouping(op, cards, current):
    groupings = []
    if len(current)>0 and current[-1] =='/' and str(cards[0]) == '0':
        return groupings
    exp = ""
    exp += str(cards[0])
    if len(cards)==1:
        current += exp
        return [current]
    exp += op
    current += exp
    groupings += final_grouping("*", cards[1:], current)
    groupings += final_grouping("/", cards[1:], current)
    groupings += final_grouping("+", cards[1:], current)
    groupings += final_grouping("-", cards[1:], current)
    return groupings

def solver(final_groupings):
    correct = []
    for group in final_groupings:
        result = eval(group)
        if result==24:
            correct.append(group)
    if len(correct)==0:
        print("There are no solutions from these 4 cards to get 24")
        return False
    else:
        print(f"There are {len(correct)} unique solutions from these 4 cards to get 24")
        print(correct)
        return True


def main():
    #cards = draw_cards()
    #print(cards)
    cards = [2,3,7,5]
    if sum(cards)==24:
        print("The sum of these cards add up to 24")
        return
    card_permutes = permuter(cards)
    processed = []
    for card_perm in card_permutes:
        ax = grouping("+", card_perm, "")
        bx = grouping("-", card_perm, "")
        cx = grouping("f", card_perm, "")
        card_groupings = ax+bx+cx
        card_groupings = grouping_formatter(card_groupings)
        card_groupings = grouping_eval(card_groupings)
        early_24_status, sol = early_24_checker(card_groupings)
        if early_24_status:
            print("There is a solution to get 24 with just addition and subtraction of the numbers")
            print(sol)
            return
        processed += card_groupings
    unique_processed = duplicate_filtering(processed)
    super_processed = single_num_filtering(unique_processed)
    final_x = []
    for superb in super_processed:
        mul_x = final_grouping('*', superb, "")
        div_x = final_grouping('/', superb, "")
        add_x = final_grouping('+', superb, "")
        sub_x = final_grouping('-', superb, "")
        womp = mul_x + div_x + add_x + sub_x
        final_x += womp
    final_x = list(set(final_x))
    return solver(final_x)

"""
Changes to make:

1.Keep track of the exact groupings/operations from start to end that results in successfully obtaining 24

2. Fix failure case #3

Failure case #1: [6, 10, 6, 7] can get 24 by (10-7)=3, then 3*6+6=24. FIXED
Failure case #2: [5, 5, 4, 9] can get 24 by (9-5)=4, 4*5+4=24. FIXED
Failure case #3: [10, 3, 10, 9] can get 24 by 10/10=1, 3*(9-1)=24. In full, it would be 3*(9-10/10)
Failure case #4: [1, 5, 7, 4] can get 24 by 7*4=28, 28-5+1=24. FIXED
Failure case #5: [2, 3, 7, 5] can get 24 by 7*3=21, 21+5-2=24. FIXED

There may be more failure cases that have not yet been found, but the above 5 are just the ones discovered through some brief testing of the very first complete initial version.
These 5 failures are likely very representative of most (if not all) failure cases. 4 of the above cases have been rectified through modifications to the algorithm, but there is
still one remaining case (#3) to be addressed.
"""
    
if __name__ == '__main__':
    main()
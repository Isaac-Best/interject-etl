

# reverse a string
def reverse_mine(string_input):
    build_string = []

    for index in range(len(string_input) -1, -1, -1):
        build_string.append(string_input[index])
    
    return ''.join(build_string)


# perfect change 
# [25, 25, 25, 25, 10, 10, 1, 1, 1]
# coins wont be in order 
def perfect_change(input_num, change_array):
    change_array.sort(reverse=True) # asc / desc

    coins_array = [0] * len(change_array)

    # 123 / 25 = 4.something
    # 123 %  25 = 23 

    for idx in range(len(change_array)):
        coins_array[idx] = input_num // change_array[idx]
        input_num = input_num % change_array[idx]

        if input_num == 0:
            break
    
    return_array = []
    #[4, 2, 0, 3,]
    for index in enumerate(coins_array):
        # (0, 4)
        # (1, 2)
        for _ in range(index[1]):
            return_array.append(change_array[index[0]])
    
    return return_array

# print(perfect_change(123, [25, 10, 5, 1]))

# finds the difference of 2 list
# takes in 2 list, same type of elements 
# return exclusive elements from both list 
list_1 = [1, 1, 2, 3]
list_2 = [2, 3]

def list_difference(list_1, list_2):

    set_1 = set(list_1)
    set_2 = set(list_2)

    return_list_1 = set()
    return_list_2 = set()

    for item in list_1:
        if item not in set_2:
            return_list_1.add(item)

    for item in list_2:
        if item not in set_1:
            return_list_2.add(item)
    
    return return_list_1, return_list_2

# print(list_difference(list_1, list_2))


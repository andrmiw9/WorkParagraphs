from collections import deque

"""
Дано:
Был (отсортированный?) список из нумерованных параграфов Word с неизвестным уровнем вложенности. Из списка удалили некоторое кол-во элементов.
Уточнение: все промежуточные уровни изначально должны присутствовать. Т.е. если есть уровень 3.1.1, то и 3.1 и 3 сущ-ют (до удаления).
Запрещается: понижать уровни: 3.1.1 -> 3.1 - так делать нельзя.
Запрещается: создавать пустые уровни, даже если 3.1.1 существует, а 3.1 не существует.
Уточнение: если параграф 2.4 стал 2.3, то и 2.4.1 становится 2.3.1

Задание: перенумеровать список
"""


def get_first_levels(input_list: list, verbose: bool = False) -> dict:
    """
    Generate a dictionary of lists where each key represents the first digit of the numbers in the input list.
    Parameters:
        input_list (list): A list of numbers.
        verbose (bool, optional): If True, print the generated dictionary of lists. Defaults to False.
    Returns:
        dict: A dictionary where the keys represent the first digit of the numbers in the input list, and the values are lists of numbers with the same first digit.
    """
    levels = {}
    digit = -1
    for t in input_list:  # distribute values by first digits
        first_digit = int(t.split('.')[0])
        if first_digit != digit:  # new digit
            digit = first_digit
            levels[digit] = [t]
        else:
            levels[digit].append(t)
    if verbose:
        print(f'First levels: {levels}')
    return levels


def get_levels_rcrsv(input_list: list, verbose: bool = False, verbose_sub: bool = False) -> dict:
    """
    Fill out levels dictionary recursively.
    Parameters:
    - input_list (list): The list to be processed.
    - verbose (bool, optional): Whether to print verbose output. Defaults to False.
    - verbose_sub (bool, optional): Whether to print verbose output for sub levels. Defaults to False.
    Returns:
    - dict: A dictionary representing the levels of the input list.
    """
    if not isinstance(input_list, list):  # check
        return None
    if verbose:
        print(f'\nGet levels input: {input_list}')

    levels = {}
    input_list = deque(input_list)
    t = input_list.popleft()  # mb empty list
    if len(t) == 0:  # check if empty list
        if len(input_list) == 0:  # no other elements
            return {0: 'End'}
        else:  # there are other elements
            levels[0] = 'End'
            t = input_list.popleft()
    digit = t[0]  # set start digit
    levels[digit] = [t[1:]]  # set start data

    for t in input_list:  # distribute values by first digits
        if verbose:
            print(f't: \t{t}')
        if t[0] != digit:  # new digit
            # print(f'NEW DIGIT')   # debug print
            digit = t[0]  # parse digit
            levels[digit] = [t[1:]]  # add to levels
        else:  # already known digit
            # print(f'OLD DIGIT')   # debug print
            levels[digit].append(t[1:])
    if verbose:
        print(f'recrsv levels: {levels}')

    for entry in levels:  # rcrsv call to get sub levels
        res = get_levels_rcrsv(levels[entry], verbose=verbose_sub, verbose_sub=verbose_sub)
        if res:
            if verbose:
                print(f'Sub res: {res}')
            levels[entry] = res

    return levels


def rebuild_list_rcrsv(levels: dict, part_res: str, verbose: bool = False):
    """
    Recursively rebuilds a list based on the levels dictionary. Implemented as generator.
    Args:
        levels (dict): A dictionary representing the levels of the list.
        part_res (str): The partial result of the list being rebuilt.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    Yields:
        str: The rebuilt list.
    """
    if not part_res:
        part_res = ''
    if type(levels) != dict:
        if verbose:
            print(f'rebuild_list_rcrsv: levels is not dict')
        return

    for entry in levels:
        if entry == 0:
            t = part_res
            part_res = part_res[:-1]
            if verbose:
                print(f'Result: {part_res}')
            yield part_res
            part_res = t
            continue
        yield from rebuild_list_rcrsv(levels[entry], part_res + str(entry) + '.', verbose=verbose)


def print_graph_keys_rcrsv(data, tabs: int = 0) -> None:  # recursive f to print all keys of nested dictionaries
    """
    A recursive function to print all keys of nested dictionaries.
    Parameters:
        data (dict): The nested dictionary to be processed.
        tabs (int): The number of tabs to be used for indentation (default is 0).
    """
    if type(data) == dict:
        for k in data.keys():
            print(tabs * '\t' + str(k))
            print_graph_keys_rcrsv(data[k], tabs + 1)


def derank_rcrsv(levels: dict, verbose: bool = False, verbose_sub: bool = False, _deepness: int = 1) -> None:
    """
    Deranks the levels dictionary recursively.
    Parameters:
    - levels (dict): The dictionary containing the levels to be deranked.
    - verbose (bool): Flag indicating whether to print verbose output. Default is False.
    - verbose_sub (bool): Flag indicating whether to print verbose output for sub-levels. Default is False.
    - _deepness (int): The current depth of recursion. Default is 1.
    """
    if not isinstance(levels, dict):
        return

    keys = sorted(levels.keys())
    if verbose:
        print(f'\n\nDerank_rcrsv! Deep: {_deepness}')
    if len(keys) == 1 and levels[keys[0]] == 'End':
        if verbose:
            print(f'Got 0: "End" dict, returning')
        return
    if verbose:
        print(f'l(keys): {keys}')

    counter = 1
    for k in keys:
        if k != 0:
            levels[counter] = levels.pop(k)
            counter += 1
    if verbose:
        print(f'\nLevels after popping: {levels}')
        print(f'\nLevels keys before deranking: {keys}')
        print(f'Levels keys after deranking: {levels.keys()}')

    for lvl in levels:
        derank_rcrsv(levels[lvl], verbose=verbose_sub, verbose_sub=verbose_sub, _deepness=_deepness + 1)


def main(input_list: list, verbose_lvl: int = 0) -> list:
    """
    Convert input list to a convenient data type and derank it. Then rebuild list in starting format and return it.
    Args:
        input_list (list): The input list to process.
        verbose_lvl (int, optional): The verbose level. Defaults to 0.
    Raises:
        ValueError: If the input list is None.
        TypeError: If the input list is not a list.
    Returns:
        list: The processed output list.
    """
    if input_list is None:
        raise ValueError('Input list is None')  # or IndexError
    if not isinstance(input_list, list):
        raise TypeError('Input list is not a list!')

    # region Prepare data

    sub_verbosing = False
    rcrsv_verbosing = False
    if verbose_lvl > 3:
        rcrsv_verbosing = True
    elif verbose_lvl > 2:
        sub_verbosing = True

    if verbose_lvl > 1:
        print(f'\n\n\nInput list: {input_list}')

    levels = get_first_levels(input_list, verbose=sub_verbosing)  # getting first levels dict
    for lvl in levels:  # for every first digit in input_list; fill levels
        res = get_levels_rcrsv([[int(t) for t in v.split('.')[1:]] for v in levels[lvl]], verbose=sub_verbosing,
                               verbose_sub=rcrsv_verbosing)
        if verbose_lvl > 1:
            print(f'\nLevel: {lvl}, res: {res}')
        levels[lvl] = res

    if verbose_lvl > 1:
        print(f'\nFinal level data:\n{levels}')
        if verbose_lvl > 3:
            print_graph_keys_rcrsv(levels)

    # endregion

    # region Deranking

    if verbose_lvl > 1:
        print(f'\n\n\nRunning derank_rcrsv')

    derank_rcrsv(levels, verbose=sub_verbosing, verbose_sub=rcrsv_verbosing)

    if verbose_lvl > 1:
        print(f'\nLevels after deranking:\n{levels}')
        print_graph_keys_rcrsv(levels)

    # endregion

    output = []
    if verbose_lvl > 2:
        print(f'\n\n\nRunning rebuild_list_rcrsv...')
    output = list(rebuild_list_rcrsv(levels, part_res='', verbose=rcrsv_verbosing))
    if verbose_lvl > 2:
        print(f'\nResult:\n{output}')

    return output


if __name__ == '__main__':
    start_l = ['2.1', '2.2.1', '2.2.3', '2.3.1.1', '2.4', '2.4.2', '2.5', '2.12.4.7', '3', '3.1', '3.1.2', '3.1.3',
               '3.2', '3.4', '3.4.1', '3.4.1.2', '3.4.2', '5', '5.2.3', '5.3.1', '5.5', '5.6', '12.1', '14']

    verbose_level = 1  # 0 - no output, 1 - only results, 2 - basic outputs, 3 - more output and 4 - recursive functions
    res = main(start_l.copy(), verbose_lvl=verbose_level)
    if verbose_level > 0:
        print(f'\n\nInput: {start_l}')
        print(f'Result: {res}')

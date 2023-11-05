from draw import draw_minimized_dfa


def minimize_dfa(transitions, start_state, accepting_states):
    # 步骤1: 划分等价状态类
    def split_into_equivalence_classes(states, transitions, alphabet):
        # 初始化等价状态类，包括接受状态和非接受状态
        equivalence_classes = [accepting_states, set(states) - accepting_states]
        new_equivalence_classes = []

        # 使用迭代循环直到不再有新的分解发生
        while equivalence_classes != new_equivalence_classes:
            new_equivalence_classes = equivalence_classes.copy()
            for i in range(len(equivalence_classes)):
                for symbol in alphabet:
                    group1 = set()
                    group2 = set()

                    # 检查每个状态的目标状态是否在同一等价类中
                    for state in equivalence_classes[i]:
                        target = transitions[state][symbol]
                        if target in equivalence_classes[i]:
                            group1.add(state)
                        else:
                            group2.add(state)

                    # 如果分成两组，则更新等价状态类
                    if group1 and group2:
                        new_equivalence_classes[i] = group1
                        new_equivalence_classes.append(group2)

            equivalence_classes = new_equivalence_classes

        return equivalence_classes

    # 步骤2: 获取新状态映射
    def get_new_state_mapping(equivalence_classes):
        state_mapping = {}
        for i, eq_class in enumerate(equivalence_classes):
            # 创建新状态标识符，例如 'S0', 'S1', 等
            new_state = f'S{i}'
            for state in eq_class:
                # 映射每个等价状态到新状态标识符
                state_mapping[state] = new_state
        return state_mapping

    # 获取字母表
    alphabet = set(symbol for transition in transitions.values() for symbol in transition.keys())

    # 步骤3: 执行等价状态划分
    equivalence_classes = split_into_equivalence_classes(transitions.keys(), transitions, alphabet)

    # 获取新状态映射
    state_mapping = get_new_state_mapping(equivalence_classes)

    # 步骤4: 构建新的最小化DFA转移函数
    new_transitions = {state_mapping[state]: {symbol: state_mapping[transitions[state][symbol]] for symbol in alphabet}
                       for state in transitions}

    # 步骤5: 更新初始状态和接受状态
    new_start_state = state_mapping[start_state]
    new_accepting_states = {state_mapping[state] for state in accepting_states}

    # 返回最小化后的DFA的转移函数、初始状态和接受状态
    return new_transitions, new_start_state, new_accepting_states


# Define your DFA transitions, start state, and accepting states
transitions = {
    'A': {'a': 'B', 'b': 'C'},
    'B': {'a': 'D', 'b': 'E'},
    'C': {'a': 'B', 'b': 'C'},
    'D': {'a': 'F', 'b': 'G'},
    'E': {'a': 'H', 'b': 'I'},
    'F': {'a': 'F', 'b': 'G'},
    'G': {'a': 'H', 'b': 'I'},
    'H': {'a': 'D', 'b': 'E'},
    'I': {'a': 'B', 'b': 'C'}
}

start_state = 'A'
accepting_states = {'F', 'H', 'I', 'G'}

# Minimize the DFA
minimized_transitions, minimized_start_state, minimized_accepting_states = minimize_dfa(transitions, start_state,
                                                                                        accepting_states)

print("Minimized DFA transitions:", minimized_transitions)
print("Minimized DFA start state:", minimized_start_state)
print("Minimized DFA accepting states:", minimized_accepting_states)

# 绘制最小化后的DFA
draw_minimized_dfa(minimized_transitions, minimized_start_state, minimized_accepting_states)

""" this program is for NFA --> DFA
    NFA is saved as a directed graph and need manually input the graph to the graph
    edges[x]:初始点为x
    edge[0]:邻接点  edge[1]:边
"""
from draw import draw_nfa


class Graph:
    node_num = 0
    edges = []
    accepting_states = set()

    def __init__(self, node_num):
        self.node_num = node_num
        for _ in range(node_num):
            self.edges.append([])

    def get_edge(self, start, end):
        for edge in self.edges[start]:
            if edge[0] == end:
                return edge[1]
        return 0  # 0 means no edge between start and end

    def get_end(self, start, val):
        ans = []
        for edge in self.edges[start]:
            if edge[1] is val:
                ans.append(edge[0])
        return ans

    def add_edge(self, start, end, value):
        self.edges[start].append([end, value])

    def add_accepting_state(self, state):
        self.accepting_states.add(state)


# Your Graph initialization goes here

graph = Graph(11)
graph.add_edge(0, 7, 'e')
graph.add_edge(0, 1, 'e')
graph.add_edge(1, 2, 'e')
graph.add_edge(1, 4, 'e')
graph.add_edge(2, 3, 'a')
graph.add_edge(4, 5, 'b')
graph.add_edge(3, 6, 'e')
graph.add_edge(5, 6, 'e')
graph.add_edge(6, 7, 'e')
graph.add_edge(7, 8, 'a')
graph.add_edge(8, 9, 'a')
graph.add_edge(8, 9, 'b')
graph.add_edge(9, 10, 'a')
graph.add_edge(9, 10, 'b')
graph.add_edge(6, 1, 'e')

# 添加接受状态
graph.add_accepting_state(10)


# Uncomment this demo graph if you want to use it


# 找邻接点集合
def move(graph, T, val):
    ans = []
    for node in T:
        ans += graph.get_end(node, val)
    return ans


def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k


def eps_cover(grpah, T):
    ans = []
    for node in T:
        ans.append(node)
    for node in T:
        next_eps = graph.get_end(node, 'e')
        for nodee in next_eps:
            if nodee not in ans:
                ans.append(nodee)
        for nodeee in eps_cover(graph, next_eps):
            if nodeee not in ans:
                ans.append(nodeee)
    ans.sort()
    return ans


if __name__ == '__main__':  # start convert
    state_name = {}
    state_change = {}
    new_set = {}
    wait = []
    wait.append(eps_cover(graph, [0]))
    i = 0
    total = 0

    name = 64
    while 1:
        curr_state = wait[i]
        name += 1
        state_name[chr(name)] = curr_state
        father = chr(name)
        change = []

        a = eps_cover(graph, move(graph, curr_state, 'a'))
        change.append(a)

        b = eps_cover(graph, move(graph, curr_state, 'b'))
        change.append(b)

        if a not in wait:
            wait.append(a)
            total += 1
        if b not in wait:
            wait.append(b)
            total += 1

        i += 1
        state_change[father] = change

        if total < i:
            break

    name_set = []
    for key, value in state_name.items():
        name_set.append(str(key))
        print(key, value)

    print('\n\n')

    dfa_transitions = []
    dfa_dic = {}
    for key, value in state_change.items():
        curr_dic = {'a': get_key(state_name, value[0]), 'b': get_key(state_name, value[1])}
        dfa_transitions.append((key, get_key(state_name, value[0]), 'a'))
        dfa_transitions.append((key, get_key(state_name, value[1]), 'b'))
        # print(key, get_key(state_name, value[0]), get_key(state_name, value[1]))
        dfa_dic[key] = curr_dic

    for key, value in dfa_dic.items():
        print(key, value)

    # 调用绘制NFA图的函数
    draw_nfa(name_set, dfa_transitions)

    # 将接受状态集合从NFA映射到DFA
    minimized_accepting_states_dfa = set()
    for dfa_state, nfa_states in state_name.items():
        for nfa_state in nfa_states:
            if nfa_state in graph.accepting_states:  # 使用 Graph 类中的 accepting_states 属性
                minimized_accepting_states_dfa.add(dfa_state)

    # 打印接受状态集合
    print("Minimized DFA accepting states:", minimized_accepting_states_dfa)

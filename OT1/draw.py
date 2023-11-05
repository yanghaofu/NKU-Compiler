import networkx as nx
import matplotlib.pyplot as plt


def draw_nfa(nfa_states, nfa_transitions):
    # 创建一个有向图对象
    G = nx.DiGraph()

    for state in nfa_states:
        G.add_node(state)

    for transition in nfa_transitions:
        start_state, end_state, label = transition
        G.add_edge(start_state, end_state, label=label)

    # 重命名节点为字符串形式
    mapping = {node: str(node) for node in G.nodes()}
    G = nx.relabel_nodes(G, mapping)

    # 计算节点布局
    pos = nx.spring_layout(G)

    # 在pos中添加标签信息
    node_labels = {}
    for node in G.nodes():
        node_labels[node] = str(node)

    # 绘制NFA
    labels = {}
    for edge in G.edges(data=True):
        start_state, end_state, attributes = edge
        edge_label = attributes['label']
        labels[(start_state, end_state)] = edge_label

    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=500, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # 添加边的标签

    plt.title("NFA")
    plt.show()


def draw_minimized_dfa(minimized_transitions, minimized_start_state, minimized_accepting_states):
    # 将最小化后的DFA转化成NFA的格式
    nfa_states = list(minimized_transitions.keys())
    nfa_transitions = []

    for start_state, transitions in minimized_transitions.items():
        for symbol, end_state in transitions.items():
            nfa_transitions.append((start_state, end_state, symbol))

    # 调用绘图函数
    draw_nfa(nfa_states, nfa_transitions)

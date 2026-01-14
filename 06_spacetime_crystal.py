#!/usr/bin/env python
# coding: utf-8

# In[7]:


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# === 彻底绕过 NetworkX 装饰器 Bug 的手动建图函数 ===
def create_manual_random_graph(n, p):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G.add_edge(i, j, weight=1.0)
    return G

# 设置随机种子
np.random.seed(42)
random.seed(42)

# === 激进版参数：打破冻结状态 ===
NUM_NODES = 60         # 节点少一点，看得更清楚
INITIAL_PROB = 0.25    # 初始更稠密，给引力更多机会
STEPS = 60             # 演化时间更长

# 关键调整：参数放大 5-10 倍
# 只要曲率低，马上就会被暗能量切断
GRAVITY_STRENGTH = 0.3  # 强引力：奖励三角形
DARK_ENERGY = 0.1       # 强暗能量：惩罚长程连接
CUTOFF_THRESHOLD = 0.5  # 提高门槛：弱者生存不了

class SpacetimeCrystal:
    def __init__(self):
        self.G = create_manual_random_graph(NUM_NODES, INITIAL_PROB)
        # 初始化权重
        for u, v in self.G.edges():
            self.G[u][v]['weight'] = 1.0
            
    def calculate_curvature(self, u, v):
        # 简化版 Ricci 曲率：几何重叠度
        nu = set(self.G.neighbors(u))
        nv = set(self.G.neighbors(v))
        if not nu or not nv: return -1
        
        common = len(nu & nv)
        union = len(nu | nv)
        if union == 0: return -1
        
        # Jaccard 系数
        return common / union
        
    def evolve(self):
        edges_to_remove = []
        edges_to_strengthen = []
        
        current_edges = list(self.G.edges(data=True))
        
        for u, v, data in current_edges:
            w = data['weight']
            kappa = self.calculate_curvature(u, v)
            
            # === 激进的演化方程 ===
            # 如果 kappa 是 0 (没共同邻居)，delta_w = -0.1 (快速衰减)
            # 如果 kappa 是 0.5 (强关联)，delta_w = 0.15 - 0.1 = +0.05 (增强)
            delta_w = (GRAVITY_STRENGTH * kappa) - DARK_ENERGY
            
            new_w = w + delta_w
            
            # 限制权重范围
            if new_w > 2.0: new_w = 2.0
            
            # 记录修改
            self.G[u][v]['weight'] = new_w
            
            # 判定断裂
            if new_w < CUTOFF_THRESHOLD:
                edges_to_remove.append((u, v))
                
        # 执行拓扑手术
        if edges_to_remove:
            self.G.remove_edges_from(edges_to_remove)
            
        return len(edges_to_remove)

    def measure_order(self):
        if self.G.number_of_nodes() == 0: return 0
        return nx.average_clustering(self.G)

# === 运行模拟 ===
sim = SpacetimeCrystal()

print(f"--- High Energy Simulation Start ---")
print(f"Initial Edges: {sim.G.number_of_edges()}")
print(f"Initial Order: {sim.measure_order():.4f}")

# 记录初始布局
pos_fixed = nx.circular_layout(sim.G)

history_order = []
history_edges = []

for t in range(STEPS):
    broken = sim.evolve()
    order = sim.measure_order()
    edges = sim.G.number_of_edges()
    
    history_order.append(order)
    history_edges.append(edges)
    
    # 每 10 步输出一次，监控变化
    if t % 10 == 0:
        print(f"Step {t}: Order={order:.4f}, Edges={edges} (Broken: {broken})")

print(f"--- End ---")
print(f"Final Order: {history_order[-1]:.4f}")

# === 绘图 ===
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

# 1. 初始状态
nx.draw(sim.G, pos=pos_fixed, ax=ax1, node_size=30, node_color='gray', edge_color='lightgray', alpha=0.5)
ax1.set_title("T=0: Chaos")

# 2. 演化曲线 (关键看这里)
ax2.plot(history_order, 'g-', linewidth=3, label='Geometric Order')
ax2.set_title("Phase Transition: Rise of Order")
ax2.set_xlabel("Time")
ax2.set_ylabel("Clustering Coefficient")
ax2.grid(True, alpha=0.3)

# 3. 边数变化 (看是否在减少)
ax3.plot(history_edges, 'r-', linewidth=3, label='Total Connections')
ax3.set_title("Dark Energy Cutting Links")
ax3.set_xlabel("Time")
ax3.set_ylabel("Number of Edges")
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# In[ ]:





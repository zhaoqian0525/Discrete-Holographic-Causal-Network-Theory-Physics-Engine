#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt

# === 修正版：宇宙学参数 ===
# 关键调整：
# 1. 提高初始膨胀速度 (HUBBLE_0)，模拟大爆炸初期巨大的动能
# 2. 降低暗能量系数 (LAMBDA)，让它在初期不显眼，后期才发力
INITIAL_SIZE = 50.0
HUBBLE_0 = 3.0        # 初始惯性很大
GRAVITY_DRAG = 0.05   # 引力导致的减速率
LAMBDA_DHCN = 0.008   # 网络自然增殖率 (较小)

TIME_STEPS = 150

class CosmicEvolution:
    def __init__(self):
        self.size = INITIAL_SIZE
        self.velocity_history = []
        self.time_history = []
        
    def run(self):
        # 初始速度完全由大爆炸惯性提供
        v_matter = HUBBLE_0
        
        for t in range(TIME_STEPS):
            # 1. 物质项 (Matter Component): 随时间衰减
            # 模拟引力把膨胀拉慢
            v_matter = v_matter / (1 + GRAVITY_DRAG)
            
            # 2. DHCN 暗能量项 (Network Growth): 随空间增大
            # 空间越大，新生的节点越多
            v_dark_energy = self.size * LAMBDA_DHCN
            
            # 总膨胀速度
            v_total = v_matter + v_dark_energy
            
            # 更新宇宙
            self.size += v_total
            
            # 记录
            self.velocity_history.append(v_total)
            self.time_history.append(t)

# === 运行模拟 ===
universe = CosmicEvolution()
universe.run()

# === 绘图 ===
plt.figure(figsize=(10, 6))

v_data = universe.velocity_history
t_data = universe.time_history

# 绘制膨胀速度曲线
plt.plot(t_data, v_data, 'r-', linewidth=3, label='Expansion Velocity (DHCN Model)')

# 寻找最低点 (Cosmic Jerk Point)
min_v = np.min(v_data)
min_t = np.argmin(v_data)

# 标注不同时期
plt.axvline(x=min_t, color='k', linestyle='--', alpha=0.5)

# 区域 1: 减速期
plt.text(min_t/2, min_v + 1.0, "Matter Dominated\n(Decelerating)", 
         color='blue', ha='center', fontweight='bold')
plt.arrow(10, v_data[10], 10, -0.5, head_width=0.1, color='blue')

# 区域 2: 加速期
plt.text(min_t + (TIME_STEPS-min_t)/2, min_v + 1.0, "Dark Energy Dominated\n(Accelerating)", 
         color='red', ha='center', fontweight='bold')
plt.arrow(120, v_data[120], 10, 0.5, head_width=0.1, color='red')

# 标注转折点
plt.annotate('Cosmic Jerk\n(Transition Point)', 
             xy=(min_t, min_v), 
             xytext=(min_t, min_v - 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

plt.title("The History of Cosmic Expansion: Deceleration to Acceleration", fontsize=14)
plt.xlabel("Cosmic Time (Billions of Years)")
plt.ylabel("Expansion Velocity (dL/dt)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()


# In[ ]:





# In[ ]:






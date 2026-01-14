#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

# === DHCN 理论核心参数 ===
# 设定光速 c = 1.0 (归一化单位)
C = 1.0
# 设定宇宙最大处理频率 Omega_max (总带宽)
# 这个值代表网络每秒能进行的最大操作数
OMEGA_MAX = 100.0  # <--- 修正处：去掉了 'Let'

class NetworkAgent:
    """
    代表 DHCN 网络中的一个基本物理实体（如粒子）。
    """
    def __init__(self, name, velocity_vector):
        self.name = name
        # 空间速度向量 v
        self.velocity = np.array(velocity_vector, dtype=float)
        # 计算标量速率 |v|
        self.speed = np.linalg.norm(self.velocity)
        
        # DHCN 约束检查：速度不能超过光速
        if self.speed >= C:
            print(f"Warning: {self.name} speed exceeds C. Clamping to 0.999C.")
            self.speed = 0.999 * C
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.speed

        # 内部时钟计数器 (记录本征时间流逝)
        self.internal_clock_ticks = 0.0
        # 记录历史数据用于绘图
        self.clock_history = []

    def update_step(self, dt_global):
        """
        模拟一个全局时间步，执行 DHCN 第一定律的带宽分配。
        dt_global: 全局网络参考系的时间步长
        """
        # --- DHCN 第一定律：带宽分配 ---
        
        # 1. 计算空间位移所需的带宽 (f_x)
        # 速度越快，占用的空间刷新频率越高
        # 归一化到最大带宽: f_x = (v/c) * OMEGA_MAX
        frequency_spatial = (self.speed / C) * OMEGA_MAX
        
        # 2. 根据守恒定律计算剩余的内部刷新带宽 (f_tau)
        # 公式: f_tau^2 + f_x^2 = OMEGA_MAX^2
        # 因此: f_tau = sqrt(OMEGA_MAX^2 - f_x^2)
        # 这在数学上等价于 f_tau = OMEGA_MAX * sqrt(1 - v^2/c^2)
        # 也就是 OMEGA_MAX / gamma (洛伦兹因子)
        # 增加 abs 防止浮点数误差导致负数
        frequency_internal = np.sqrt(np.abs(OMEGA_MAX**2 - frequency_spatial**2))
        
        # 3. 更新内部时钟
        # 在这个全局时间步 dt_global 内，内部时钟增加了 f_tau * dt 个滴答
        ticks_gained = frequency_internal * dt_global
        self.internal_clock_ticks += ticks_gained
        
        self.clock_history.append(self.internal_clock_ticks)

# === 运行模拟实验 ===

# 初始化模拟参数
total_global_time = 10.0  # 模拟总时长（全局参考系）
time_step = 0.01          # 时间步长
steps = int(total_global_time / time_step)
global_time_axis = np.linspace(0, total_global_time, steps)

# 创建两个对比代理
# Agent A: 静止 (速度 = 0)
agent_static = NetworkAgent(name="Static Observer (v=0)", velocity_vector=[0, 0])

# Agent B: 高速运动 (速度 = 0.8c)
# 根据相对论预测，其时间流逝速度应为静止者的 sqrt(1-0.8^2) = 0.6 倍
agent_fast = NetworkAgent(name="Fast Traveler (v=0.8c)", velocity_vector=[0.8*C, 0])

print(f"--- DHCN Simulation Start ---")
print(f"System Bandwidth (Omega): {OMEGA_MAX} Hz")
print(f"Agent A Speed: {agent_static.speed/C:.1f}c")
print(f"Agent B Speed: {agent_fast.speed/C:.1f}c")

# 主循环
for _ in range(steps):
    agent_static.update_step(time_step)
    agent_fast.update_step(time_step)

print(f"--- Simulation End ---")
print(f"Final Internal Clock (Static): {agent_static.internal_clock_ticks:.2f} ticks")
print(f"Final Internal Clock (Fast):   {agent_fast.internal_clock_ticks:.2f} ticks")

# 防止除零错误
if agent_static.internal_clock_ticks > 0:
    ratio = agent_fast.internal_clock_ticks / agent_static.internal_clock_ticks
    print(f"Time Dilation Ratio (Fast/Static): {ratio:.4f}")
    print(f"Theoretical Prediction (sqrt(1-v^2/c^2)): {np.sqrt(1 - 0.8**2):.4f}")
else:
    print("Error: Static clock did not tick.")

# === 结果可视化 ===
plt.figure(figsize=(10, 6))

# 绘制基准线（如果拥有全部带宽，时钟应达到的滴答数）
theoretical_max_ticks = OMEGA_MAX * global_time_axis
plt.plot(global_time_axis, theoretical_max_ticks, 'k--', alpha=0.3, label='Max Possible Bandwidth')

# 绘制代理的内部时钟积累
plt.plot(global_time_axis, agent_static.clock_history, 'b-', linewidth=2, label=f'{agent_static.name}')
plt.plot(global_time_axis, agent_fast.clock_history, 'r-', linewidth=2, label=f'{agent_fast.name}')

# 图表修饰
plt.title("Verification of DHCN First Law: Bandwidth Conservation", fontsize=14)
plt.xlabel("Global Network Time", fontsize=12)
plt.ylabel("Proper Time (Internal Ticks)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11)
plt.tight_layout()

# 显示结果
plt.show()


# In[ ]:





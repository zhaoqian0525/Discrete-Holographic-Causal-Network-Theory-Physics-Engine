#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt

# === DHCN 理论核心参数 ===
C = 1.0          # 光速
OMEGA_MAX = 100.0 # 总带宽
REST_MASS = 1.0   # 代理的静止质量 (设定为 1.0 以简化计算)

class DynamicAgent:
    """
    一个可以受力加速的 DHCN 代理
    """
    def __init__(self, name):
        self.name = name
        self.speed = 0.0
        self.momentum = 0.0 # 动量 p
        self.internal_clock = 0.0
        
        # 用于记录数据的列表
        self.hist_time = []
        self.hist_speed = []
        self.hist_acceleration = []
        self.hist_inertia = [] # 记录有效惯性 (相对论质量)

    def apply_force_and_update(self, force, dt):
        """
        核心物理引擎：施加力，更新动量，受带宽限制解算出新的速度
        """
        # 1. 力改变动量 (牛顿第二定律的原始形式 F = dp/dt)
        # 我们施加一个恒定的力，动量线性增加
        self.momentum += force * dt
        
        # 2. 关键步骤：从动量反推速度
        # 在相对论/DHCN中，p = gamma * m * v = v / sqrt(1 - v^2/c^2) * m
        # 解出 v，得到公式: v = p / sqrt(m^2*c^2 + p^2/c^2)
        # 这个公式体现了光速限制：无论 p 多大，v 永远小于 c
        old_speed = self.speed
        self.speed = self.momentum / np.sqrt((REST_MASS*C)**2 + (self.momentum/C)**2)
        
        # 3. 计算瞬时加速度 (a = dv/dt)
        acceleration = (self.speed - old_speed) / dt
        
        # 4. 计算有效惯性 (Effective Inertia)
        # 即此时此刻要把物体推动，它表现出的"质量"。
        # 根据 F = m_eff * a  =>  m_eff = F / a
        # 在低速时它应该接近 REST_MASS (1.0)，高速时趋于无穷大
        effective_inertia = force / acceleration if acceleration > 1e-9 else np.inf

        # --- DHCN 带宽核算 (用于验证时间膨胀) ---
        frequency_spatial = (self.speed / C) * OMEGA_MAX
        frequency_internal = np.sqrt(np.abs(OMEGA_MAX**2 - frequency_spatial**2))
        self.internal_clock += frequency_internal * dt

        # 记录数据
        self.hist_speed.append(self.speed)
        self.hist_acceleration.append(acceleration)
        self.hist_inertia.append(effective_inertia)

# === 运行动力学模拟 ===

# 初始化
total_time = 20.0
dt = 0.01
steps = int(total_time / dt)
time_axis = np.linspace(0, total_time, steps)

# 创建代理并施加恒定推力
agent = DynamicAgent("Rocket")
CONSTANT_FORCE = 0.5 # 施加一个恒定的力

print(f"--- Starting Acceleration Test ---")
print(f"Applied Constant Force: {CONSTANT_FORCE}")
print(f"Agent Rest Mass: {REST_MASS}")

for t in time_axis:
    agent.apply_force_and_update(CONSTANT_FORCE, dt)
    agent.hist_time.append(t)

print(f"--- End Test ---")
print(f"Final Speed: {agent.speed:.4f} c")
print(f"Final Acceleration: {agent.hist_acceleration[-1]:.6f}")
print(f"Final Effective Inertia: {agent.hist_inertia[-1]:.4f}")

# === 可视化结果 (双图展示) ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# 图1：速度随时间的变化
# 展示牛顿预测（线性增加）与 DHCN 预测（光速封顶）的对比
newtonian_speed = (CONSTANT_FORCE / REST_MASS) * time_axis
ax1.plot(time_axis, newtonian_speed, 'k--', alpha=0.5, label='Newtonian Prediction (v=at)')
ax1.plot(time_axis, [C]*len(time_axis), 'r:', label='Speed of Light (c)')
ax1.plot(time_axis, agent.hist_speed, 'b-', linewidth=3, label='DHCN Agent Speed')
ax1.set_title("Velocity vs. Time under Constant Force")
ax1.set_ylabel("Speed (c)")
ax1.set_ylim(0, 1.5)
ax1.legend()
ax1.grid(True)

# 图2：惯性（有效质量）随速度的变化
# 展示随着速度接近光速，推动它变得多么困难
ax2.plot(agent.hist_speed, agent.hist_inertia, 'r-', linewidth=3, label='Effective Inertia (Relativistic Mass)')
ax2.axhline(y=REST_MASS, color='k', linestyle='--', label='Rest Mass (Newtonian Inertia)')
ax2.set_title("The Cost of Acceleration: Inertia Increases with Speed")
ax2.set_xlabel("Speed (c)")
ax2.set_ylabel("Effective Inertia / Mass")
ax2.set_yscale('log') # 使用对数坐标轴以显示巨大变化
ax2.set_xlim(0, 1.0)
ax2.legend()
ax2.grid(True, which="both", ls="--")

plt.tight_layout()
plt.show()


# In[ ]:





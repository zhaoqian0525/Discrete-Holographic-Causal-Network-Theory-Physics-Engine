#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt

# === DHCN 理论参数 ===
G_NEWTON = 1.0   # 标准引力常数
MASS_GALAXY = 1000.0 # 星系中心质量 (黑洞+恒星盘)
ALPHA = 2.0      # DHCN 纠缠修正系数 (对应全息熵的对数项)

def newtonian_velocity(r):
    """
    标准牛顿预测：v = sqrt(GM / r)
    随距离增加，速度应该衰减。
    """
    # 防止除零
    r = np.maximum(r, 0.1)
    v = np.sqrt(G_NEWTON * MASS_GALAXY / r)
    return v

def dhcn_entropic_velocity(r):
    """
    DHCN 预测：熵力包含长程修正
    F_total = F_Newton + F_Entropic
    ma = GM/r^2 + (Alpha * sqrt(GM))/r  <-- 1/r 衰减项
    
    推导速度 v:
    v^2/r = F_total / m
    v^2/r = GM/r^2 + C/r
    v^2 = GM/r + C
    v = sqrt(GM/r + C) -> 当 r 很大时，v 趋于常数
    """
    r = np.maximum(r, 0.1)
    
    # 1. 牛顿项 (短程主导)
    term_newton = G_NEWTON * MASS_GALAXY / r
    
    # 2. DHCN 熵力修正项 (长程主导)
    # 这一项源于 S ~ Area + ln(Area) 的修正
    # 导致一个恒定的背景加速度 a0
    # 为简化模拟，我们设定修正项贡献一个渐进常数速度
    term_entropic = ALPHA # 这是一个简化的常数项模拟
    
    v = np.sqrt(term_newton + term_entropic)
    return v

# === 模拟实验 ===
# 设定从星系中心到边缘的距离 (0 到 100 单位)
radii = np.linspace(1, 100, 200)

# 计算速度曲线
v_newton = newtonian_velocity(radii)
v_dhcn = dhcn_entropic_velocity(radii)

# === 模拟观测数据 (制造一些带噪声的"真实"数据点) ===
# 假设真实宇宙遵循 DHCN 规律，我们来看看天文学家观测到了什么
np.random.seed(42)
obs_radii = np.linspace(5, 95, 20)
obs_velocity = dhcn_entropic_velocity(obs_radii) + np.random.normal(0, 0.2, 20)

# === 可视化 ===
plt.figure(figsize=(10, 6))

# 1. 绘制牛顿预测 (虚线)
plt.plot(radii, v_newton, 'k--', label='Newtonian Prediction (Expected Decay)')

# 2. 绘制 DHCN 预测 (实线)
plt.plot(radii, v_dhcn, 'r-', linewidth=2.5, label='DHCN Prediction (Entropic Correction)')

# 3. 绘制"观测数据" (散点)
plt.errorbar(obs_radii, obs_velocity, yerr=0.3, fmt='bo', label='Galaxy Observation Data', alpha=0.6)

# 图表修饰
plt.title("Galaxy Rotation Curve: Newton vs. DHCN", fontsize=14)
plt.xlabel("Distance from Galaxy Center (r)", fontsize=12)
plt.ylabel("Orbital Velocity (v)", fontsize=12)
plt.axhline(y=np.sqrt(ALPHA), color='g', linestyle=':', label='DHCN Asymptotic Velocity')
plt.text(80, np.sqrt(ALPHA)+0.5, "Flat Rotation!", color='g', fontweight='bold')

plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[4]:


# === 视觉增强版参数设置 ===
G = 1.0
MASS = 5000.0  # 增加中心质量，让起始速度很高
ALPHA = 25.0   # 增加 DHCN 的修正力度，让尾部明显翘起

def get_newton_curve(r):
    # 牛顿预测：速度随距离平方根衰减 (v ~ 1/sqrt(r))
    # 距离越远，掉得越快
    return np.sqrt(G * MASS / r)

def get_dhcn_curve(r):
    # DHCN 预测：牛顿项 + 熵力修正项
    # 当 r 很大时，牛顿项消失，只剩下 sqrt(ALPHA)
    term_newton = G * MASS / r
    term_entropic = ALPHA  # 长程恒定背景力
    return np.sqrt(term_newton + term_entropic)

# === 生成数据 ===
# 距离从 10 到 200 (拉长距离以显示长程效应)
r = np.linspace(10, 200, 500)

v_newton = get_newton_curve(r)
v_dhcn = get_dhcn_curve(r)

# === 绘图 ===
plt.figure(figsize=(12, 7))

# 1. 绘制牛顿曲线 (蓝色虚线 - 下滑)
plt.plot(r, v_newton, color='blue', linestyle='--', linewidth=2, label='Newtonian (Expected Decay)')

# 2. 绘制 DHCN 曲线 (红色实线 - 平坦)
plt.plot(r, v_dhcn, color='red', linewidth=3, label='DHCN (Entropic Correction)')

# 3. 关键：填充两条线之间的区域 (视觉化"暗物质"的需求量)
plt.fill_between(r, v_newton, v_dhcn, color='gray', alpha=0.15, label='The "Dark Matter" Gap')

# 4. 添加标注箭头，解释发生了什么
plt.annotate('Newton says: Speed should drop!', xy=(180, v_newton[-1]), xytext=(120, 5),
             arrowprops=dict(facecolor='blue', shrink=0.05), fontsize=10, color='blue')

plt.annotate('Reality/DHCN: Speed stays high!', xy=(180, v_dhcn[-1]), xytext=(120, 25),
             arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')

plt.annotate('Correction Term', xy=(100, (v_newton[250]+v_dhcn[250])/2), ha='center', fontsize=9, color='gray')

# 图表修饰
plt.title("Visualizing the 'Gap': Why Newton Fails & DHCN Works", fontsize=15)
plt.xlabel("Distance from Galaxy Center", fontsize=12)
plt.ylabel("Rotation Velocity", fontsize=12)
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, alpha=0.3)
plt.ylim(0, 30) # 锁定 Y 轴范围，让下降趋势更明显

plt.show()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import matplotlib.pyplot as plt

# === DIPT 5.0: 路径积分核心验证 ===
# 我们直接计算从缝隙到屏幕每一个像素点的“路径长度”
# 这模拟了 DHCN 网络底层的寻路算法

# 1. 实验几何设置
SCREEN_WIDTH = 1000      # 屏幕分辨率 (像素点)
WAVELENGTH = 20.0        # 波长
SLIT_DISTANCE = 120.0    # 双缝间距 (d)
SCREEN_DISTANCE = 2000.0 # 屏幕距离 (L) -> 确保进入远场
K = 2 * np.pi / WAVELENGTH # 波数

# 屏幕上的坐标点 Y
y = np.linspace(-400, 400, SCREEN_WIDTH)

# 2. 计算路径长度 (Path Length)
# r1: 从上缝到屏幕点 y 的距离
# r2: 从下缝到屏幕点 y 的距离
r1 = np.sqrt(SCREEN_DISTANCE**2 + (y - SLIT_DISTANCE/2)**2)
r2 = np.sqrt(SCREEN_DISTANCE**2 + (y + SLIT_DISTANCE/2)**2)

# 3. 计算格林函数 (Green's Function) / 传播子
# DIPT 网络传递的信息流：Psi = (1/r) * exp(i * k * r)
psi_1 = (1/r1) * np.exp(1j * K * r1)
psi_2 = (1/r2) * np.exp(1j * K * r2)

# === 模式 A: 未观测态 (Wave / Computation Mode) ===
# 网络执行复数叠加 (保留相位)
# Psi_total = Psi_1 + Psi_2
psi_total = psi_1 + psi_2
intensity_wave = np.abs(psi_total)**2

# === 模式 B: 观测态 (Particle / Refresh Mode) ===
# 网络执行概率叠加 (丢失相位)
# I_total = |Psi_1|^2 + |Psi_2|^2
intensity_particle = np.abs(psi_1)**2 + np.abs(psi_2)**2

# === 归一化处理 ===
# 为了直观对比，我们将单缝强度的峰值归一化
max_single = np.max(np.abs(psi_1)**2)
intensity_wave /= max_single
intensity_particle /= max_single

# === 数据探针 ===
center_idx = SCREEN_WIDTH // 2
peak_wave = intensity_wave[center_idx]
peak_particle = intensity_particle[center_idx]

print("\n>>> DIPT PATH INTEGRAL VERIFICATION <<<")
print(f"1. Center Intensity (Wave):     {peak_wave:.4f}")
print(f"2. Center Intensity (Particle): {peak_particle:.4f}")
print(f"3. Constructive Ratio: {peak_wave/peak_particle:.4f} (Theoretical Target: 2.0)")
print("   (解释: 波的叠加是 (1+1)^2=4，粒子的叠加是 1^2+1^2=2。比值为 2.0)")

# === 绘图 ===
plt.figure(figsize=(12, 7))

# 绘制波模式 (蓝色实线)
plt.plot(y, intensity_wave, 'b-', linewidth=2.5, label='Unobserved (Wave Interference)')
plt.fill_between(y, intensity_wave, color='blue', alpha=0.1)

# 绘制粒子模式 (红色虚线)
plt.plot(y, intensity_particle, 'r--', linewidth=3, label='Observed (Particle Sum)')

plt.title(f"DIPT Final Verification: Path Integral Summation\n(Ratio = {peak_wave/peak_particle:.2f})", fontsize=15)
plt.xlabel("Screen Position")
plt.ylabel("Normalized Intensity")
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, alpha=0.3)

# 标注
plt.annotate('Perfect Constructive Interference\n(Signal Amplified)', 
             xy=(0, peak_wave), 
             xytext=(50, peak_wave),
             arrowprops=dict(facecolor='blue', shrink=0.05), fontsize=10, color='blue')

plt.annotate('No Interference\n(Simple Sum)', 
             xy=(0, peak_particle), 
             xytext=(50, peak_particle),
             arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')

# 标注第一个波谷 (相消干涉)
# 理论波谷位置
min_idx = np.argmin(intensity_wave[center_idx-50:center_idx+50]) + center_idx - 50
plt.annotate('Destructive Interference\n(Zero Signal)', 
             xy=(y[min_idx], 0), 
             xytext=(y[min_idx]+50, 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)

plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





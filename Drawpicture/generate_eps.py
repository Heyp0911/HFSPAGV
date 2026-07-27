import matplotlib
matplotlib.use('Agg') # 解决 backend_interagg 报错的关键

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 创建画布，设置比例
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off') # 隐藏坐标轴

# 定义主题颜色
color_s1 = '#AEC6E8' # 阶段1：浅蓝色
color_s2 = '#98DF8A' # 阶段2：浅绿色
color_sc = '#D3D3D3' # 阶段C：浅灰色

# 绘制矩形框的辅助函数
def draw_box(x, y, w, h, text, color='white', text_size=12, edge='black'):
    # 添加矩形
    rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=edge, facecolor=color, zorder=2)
    ax.add_patch(rect)
    # 添加文本，如果宽高比说明是竖直框，则旋转文字
    rotation = 90 if w < h else 0
    if text:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=text_size,
                weight='bold' if 'QUEUE' in text or 'WORK' in text else 'normal',
                zorder=3, rotation=rotation)

# 1. 绘制左右两侧的队列和完成框
draw_box(1, 2, 1, 6, "JOB QUEUE", text_size=14)
draw_box(16, 2, 1, 6, "COMPLETED\nWORKPIECES", text_size=14)

# 2. 绘制阶段标题
ax.text(5, 9, "STAGE 1", ha='center', va='center', fontsize=16, weight='bold')
ax.text(9, 9, "STAGE 2", ha='center', va='center', fontsize=16, weight='bold')
ax.text(13, 9, "STAGE C", ha='center', va='center', fontsize=16, weight='bold')

# 3. 绘制各个阶段的机器节点
# Stage 1
draw_box(4, 7, 2, 1.2, "MACHINE\n$M_{1,1}$", color=color_s1)
draw_box(4, 4.5, 2, 1.2, "MACHINE\n$M_{1,2}$", color=color_s1)
ax.text(5, 3.5, "...", ha='center', va='center', fontsize=20, weight='bold')
draw_box(4, 1.5, 2, 1.2, "MACHINE\n$M_{1,x}$", color=color_s1)

# Stage 2
draw_box(8, 7, 2, 1.2, "MACHINE\n$M_{2,1}$", color=color_s2)
draw_box(8, 4.5, 2, 1.2, "MACHINE\n$M_{2,2}$", color=color_s2)
ax.text(9, 3.5, "...", ha='center', va='center', fontsize=20, weight='bold')
draw_box(8, 1.5, 2, 1.2, "MACHINE\n$M_{2,y}$", color=color_s2)

# Stage C
draw_box(12, 7, 2, 1.2, "MACHINE\n$M_{C,1}$", color=color_sc)
draw_box(12, 4.5, 2, 1.2, "MACHINE\n$M_{C,2}$", color=color_sc)
ax.text(13, 3.5, "...", ha='center', va='center', fontsize=20, weight='bold')
draw_box(12, 1.5, 2, 1.2, "MACHINE\n$M_{C,z}$", color=color_sc)

# 绘制箭头的辅助函数
def draw_arrow(x1, y1, x2, y2, style='-'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5, ls=style), zorder=1)

# 4. 连线 (复刻原图逻辑)
# 从 Job Queue 到 Stage 1
draw_arrow(2, 5, 4, 7.6)
draw_arrow(2, 5, 4, 5.1)
draw_arrow(2, 5, 4, 2.1, style='--')

# 从 Stage 1 到 Stage 2 (错综复杂的路由关系)
draw_arrow(6, 7.6, 8, 7.6)               # M11 -> M21
draw_arrow(6, 7.6, 8, 5.1, style='--')   # M11 -> M22
draw_arrow(6, 7.6, 8, 2.1, style='--')   # M11 -> M2y

draw_arrow(6, 5.1, 8, 7.4, style='--')   # M12 -> M21
draw_arrow(6, 5.1, 8, 2.3, style='--')   # M12 -> M2y

draw_arrow(6, 2.1, 8, 7.2, style='--')   # M1x -> M21
draw_arrow(6, 2.1, 8, 1.9, style='--')   # M1x -> M2y

# 从 Stage 2 到 Stage C (中间包含省略号跨度)
ax.text(11, 7.6, "...", ha='center', va='center', fontsize=20)
ax.text(11, 5.1, "...", ha='center', va='center', fontsize=20)
ax.text(11, 2.1, "...", ha='center', va='center', fontsize=20)

draw_arrow(10, 7.6, 10.6, 7.6, style='--')
draw_arrow(11.4, 7.6, 12, 7.6, style='--')

draw_arrow(10, 5.1, 10.6, 5.1, style='--')
draw_arrow(11.4, 5.1, 12, 5.1, style='--')

draw_arrow(10, 2.1, 10.6, 2.1)
draw_arrow(11.4, 2.1, 12, 2.1)

# 从 Stage C 到 Completed Workpieces
draw_arrow(14, 7.6, 16, 5, style='--')
draw_arrow(14, 5.1, 16, 5, style='--')
draw_arrow(14, 2.1, 16, 5, style='--')

# 5. 保存并输出为高精度 EPS
plt.savefig('flow_shop_diagram.eps', format='eps', bbox_inches='tight')
print("EPS 图片已成功生成并保存为 'flow_shop_diagram.eps'")
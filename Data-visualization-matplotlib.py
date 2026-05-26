import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 1. Setup charts directory
CHARTS_DIR = "charts"
if not os.path.exists(CHARTS_DIR):
    os.makedirs(CHARTS_DIR)
    print(f"Created directory: '{CHARTS_DIR}' to save charts.")

# 2. Load clean data
DATA_FILE = "global_tech_salary_clean.csv"
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Cleaned data file not found: {DATA_FILE}. Please run preprocess_salary.py first.")

print(f"Loading data from '{DATA_FILE}'...")
df = pd.read_csv(DATA_FILE)

# General plotting configuration
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# Colors for experience levels
COLORS_EXP = {'EN': '#5D9CEC', 'MI': '#4FC1E9', 'SE': '#AC92EC', 'EX': '#EC87C0'}
# Colors for company size
COLORS_SIZE = {'S': '#FC6E51', 'M': '#A0D468', 'L': '#48CFAD'}


# ==============================================================================
# 1. RELATIONSHIP CHART (Hybrid Box Plot + Jittered Scatter Plot)
# ==============================================================================
print("Plotting Relationship chart (Hybrid Box + Jittered Scatter)...")
fig, ax = plt.subplots(figsize=(9, 7))

# Map experience level to numeric scale and add horizontal jitter
exp_order = ['EN', 'MI', 'SE', 'EX']
exp_labels = ['Entry-level (EN)', 'Mid-level (MI)', 'Senior-level (SE)', 'Executive (EX)']
df['exp_numeric'] = df['experience_level'].map({'EN': 0, 'MI': 1, 'SE': 2, 'EX': 3})

np.random.seed(42)
jitter = np.random.normal(0, 0.12, size=len(df))
df['exp_jitter'] = df['exp_numeric'] + jitter

# Draw boxplots underneath
box_data = [df[df['experience_level'] == exp]['salary_in_usd'] for exp in exp_order]
bp = ax.box_plot = ax.boxplot(box_data, positions=[0, 1, 2, 3], patch_artist=True,
                             showfliers=False,
                             medianprops=dict(color='#333333', linewidth=2),
                             boxprops=dict(facecolor='#E6E9ED', color='#AAB2BD', alpha=0.5, linewidth=1.5),
                             whiskerprops=dict(color='#AAB2BD', linewidth=1.5),
                             capprops=dict(color='#AAB2BD', linewidth=1.5))

# Draw individual points on top
for i, exp in enumerate(exp_order):
    group = df[df['experience_level'] == exp]
    ax.scatter(group['exp_jitter'], group['salary_in_usd'], alpha=0.5, 
               label=exp_labels[i], color=COLORS_EXP[exp], edgecolors='none', s=25, zorder=3)

# Configure axes
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(exp_labels, fontsize=10, fontweight='bold')
ax.set_xlabel('Cấp bậc kinh nghiệm (Experience Level)', fontsize=11, fontweight='bold', labelpad=12)
ax.set_ylabel('Mức lương trong năm (USD)', fontsize=11, fontweight='bold', labelpad=12)
ax.set_title('1. Relationship: Phân bố & Mối quan hệ giữa Cấp bậc & Lương USD', fontsize=14, fontweight='bold', pad=18)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(title='Cấp bậc kinh nghiệm', loc='upper left', frameon=True)

plt.tight_layout()
relationship_path = os.path.join(CHARTS_DIR, "1_relationship.png")
plt.savefig(relationship_path, dpi=300)
plt.close()
print(f"-> Saved: {relationship_path}")


# ==============================================================================
# 2. TREND CHART (2 Subplots: Experience Levels & Top Job Titles)
# ==============================================================================
print("Plotting Trend chart (Experience Levels vs Top Job Titles)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subplot 1: Experience Level trends over years
# Plot both mean and median to account for skewness in salary distribution
trend_exp_mean = df.groupby(['work_year', 'experience_level'])['salary_in_usd'].mean().unstack()
trend_exp_median = df.groupby(['work_year', 'experience_level'])['salary_in_usd'].median().unstack()
for exp in exp_order:
    if exp in trend_exp_mean.columns:
        ax1.plot(trend_exp_mean.index, trend_exp_mean[exp], marker='o', linewidth=2.5,
                 label=f"{exp} Mean", color=COLORS_EXP[exp])
    if exp in trend_exp_median.columns:
        ax1.plot(trend_exp_median.index, trend_exp_median[exp], marker='o', linestyle='--', linewidth=1.5,
                 label=f"{exp} Median", color=COLORS_EXP[exp], alpha=0.8)

overall_trend_mean = df.groupby('work_year')['salary_in_usd'].mean()
overall_trend_median = df.groupby('work_year')['salary_in_usd'].median()
ax1.plot(overall_trend_mean.index, overall_trend_mean.values, linestyle='-', color='#4A4A4A',
        linewidth=2, label='Overall Mean')
ax1.plot(overall_trend_median.index, overall_trend_median.values, linestyle='--', color='#4A4A4A',
        linewidth=1.5, label='Overall Median')

ax1.set_xlabel('Năm làm việc', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_ylabel('Lương trung bình (USD)', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_title('A. Xu hướng lương theo Cấp bậc kinh nghiệm', fontsize=12, fontweight='bold', pad=12)
# use the mean-based index (work_years) for xticks (both mean and median share same index)
ax1.set_xticks(trend_exp_mean.index)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(title='Phân loại', loc='upper left')

# Subplot 2: Top 4 Job Titles trends over years
top_jobs = df['job_title'].value_counts().head(4).index.tolist()
trend_jobs = df[df['job_title'].isin(top_jobs)].groupby(['work_year', 'job_title'])['salary_in_usd'].mean().unstack()

colors_jobs = ['#4A89DC', '#8CC152', '#F6BB42', '#967ADC']
for i, job in enumerate(top_jobs):
    if job in trend_jobs.columns:
        ax2.plot(trend_jobs.index, trend_jobs[job], marker='s', linewidth=2.5, 
                 label=job, color=colors_jobs[i])

ax2.set_xlabel('Năm làm việc', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_ylabel('Lương trung bình (USD)', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_title('B. Xu hướng lương theo Top 4 vị trí công việc phổ biến nhất', fontsize=12, fontweight='bold', pad=12)
ax2.set_xticks(trend_jobs.index)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(title='Vị trí công việc', loc='upper left')

fig.suptitle('2. Trend: Xu hướng thay đổi mức lương qua các năm (2020 - 2024)', fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
trend_path = os.path.join(CHARTS_DIR, "2_trend.png")
plt.savefig(trend_path, dpi=300)
plt.close()
print(f"-> Saved: {trend_path}")


# ==============================================================================
# 3. PART OF A WHOLE CHART (2 Subplots: Experience Levels & Company Sizes)
# ==============================================================================
print("Plotting Part of a Whole chart (Experience vs Company Size)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

# Subplot 1: Experience Level (use fixed order to keep colors/labels stable)
# ensure counts follow `exp_order` so colors and labels remain consistent
exp_counts = df['experience_level'].value_counts().reindex(exp_order).fillna(0).astype(int)
exp_labels_pie = [f"{label}\n({count:,} người)" for label, count in zip(exp_labels, exp_counts.values)]
colors_exp_pie = [COLORS_EXP[exp] for exp in exp_order]
wedges1, texts1, autotexts1 = ax1.pie(exp_counts.values, labels=exp_labels_pie, autopct='%1.1f%%',
                                    startangle=90, colors=colors_exp_pie, 
                                    wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2))
plt.setp(texts1, size=9, fontweight='bold')
plt.setp(autotexts1, size=9, weight="bold", color="black")
ax1.set_title('A. Tỷ lệ nhân sự theo Cấp bậc kinh nghiệm', fontsize=12, fontweight='bold', pad=10)

# Subplot 2: Company Size (use fixed order S->M->L)
size_order = ['S', 'M', 'L']
size_counts = df['company_size'].value_counts().reindex(size_order).fillna(0).astype(int)
size_mapping = {'S': 'Small (S)', 'M': 'Medium (M)', 'L': 'Large (L)'}
size_labels_pie = [f"{size_mapping[size]}\n({count:,} c.ty)" for size, count in zip(size_order, size_counts.values)]
colors_size_pie = [COLORS_SIZE[size] for size in size_order]
wedges2, texts2, autotexts2 = ax2.pie(size_counts.values, labels=size_labels_pie, autopct='%1.1f%%',
                                    startangle=90, colors=colors_size_pie, 
                                    wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2))
plt.setp(texts2, size=9, fontweight='bold')
plt.setp(autotexts2, size=9, weight="bold", color="black")
ax2.set_title('B. Cơ cấu quy mô doanh nghiệp tuyển dụng', fontsize=12, fontweight='bold', pad=10)

fig.suptitle('3. Part of a Whole: Tỷ lệ cơ cấu nhân sự và quy mô doanh nghiệp', fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
part_of_whole_path = os.path.join(CHARTS_DIR, "3_part_of_whole.png")
plt.savefig(part_of_whole_path, dpi=300)
plt.close()
print(f"-> Saved: {part_of_whole_path}")


# ==============================================================================
# 4. DISTRIBUTION CHART (2 Subplots: Hist+KDE of Salaries & Boxplot by Company Size)
# ==============================================================================
print("Plotting Distribution chart (Hist+KDE & Boxplot by Company Size)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subplot 1: Histogram + Math KDE
salaries = df['salary_in_usd'].values
# Plot histogram normalized (density=True) so KDE fits on top
n, bins, patches = ax1.hist(salaries, bins=35, color='#4A89DC', alpha=0.6, 
                            edgecolor='#357EC7', linewidth=0.5, density=True, label='Mật độ tần suất')

# Calculate mathematical KDE using scipy
kde = gaussian_kde(salaries)
x_range = np.linspace(salaries.min(), salaries.max(), 300)
ax1.plot(x_range, kde(x_range), color='#E9573F', linewidth=2.5, label='Đường mật độ KDE')

# Stats lines
mean_val = salaries.mean()
median_val = np.median(salaries)
ax1.axvline(mean_val, color='#DA4453', linestyle='dashed', linewidth=2, label=f'Mean (T.bình): ${int(mean_val):,}')
ax1.axvline(median_val, color='#8CC152', linestyle='dashdot', linewidth=2, label=f'Median (T.vị): ${int(median_val):,}')

ax1.set_xlabel('Mức lương trong năm (USD)', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_ylabel('Mật độ xác suất', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_title('A. Phân phối lương USD & Đường mật độ KDE', fontsize=12, fontweight='bold', pad=12)
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(loc='upper right')

# Subplot 2: Boxplot of salary by Company Size
size_order = ['S', 'M', 'L']
size_labels = ['Small (S)', 'Medium (M)', 'Large (L)']
box_size_data = [df[df['company_size'] == sz]['salary_in_usd'] for sz in size_order]

bp_sz = ax2.boxplot(box_size_data, patch_artist=True, showfliers=True,
                    medianprops=dict(color='#333333', linewidth=1.5),
                    whiskerprops=dict(color='#AAB2BD', linewidth=1.2),
                    capprops=dict(color='#AAB2BD', linewidth=1.2),
                    flierprops=dict(marker='o', markerfacecolor='#DA4453', markersize=3, markeredgecolor='none', alpha=0.5))

# Color boxplot patches
for patch, color in zip(bp_sz['boxes'], [COLORS_SIZE[sz] for sz in size_order]):
    patch.set_facecolor(color)
    patch.set_edgecolor('#AAB2BD')
    patch.set_alpha(0.7)
    patch.set_linewidth(1.5)

ax2.set_xticklabels(size_labels, fontsize=10, fontweight='bold')
ax2.set_xlabel('Quy mô công ty', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_ylabel('Mức lương trong năm (USD)', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_title('B. Phân tán & Khoảng lương theo Quy mô công ty', fontsize=12, fontweight='bold', pad=12)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
ax2.grid(axis='y', linestyle='--', alpha=0.4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

fig.suptitle('4. Distribution: Thống kê mô tả phân phối lương trong ngành công nghệ', fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
distribution_path = os.path.join(CHARTS_DIR, "4_distribution.png")
plt.savefig(distribution_path, dpi=300)
plt.close()
print(f"-> Saved: {distribution_path}")


# ==============================================================================
# 5. FLOW CHART (2 Subplots: Remote Work Models & Experience Level Shifts)
# ==============================================================================
print("Plotting Flow chart (Remote Shifts & Experience Shifts)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subplot 1: Remote Work shift over years
# Map known remote_ratio values safely; unknown ratios become 'Other' and are ignored in ordered stack
remote_map = {0: 'On-site (0%)', 50: 'Hybrid (50%)', 100: 'Remote (100%)'}
df['work_type'] = df['remote_ratio'].map(remote_map).fillna('Other')
flow_remote = df.groupby(['work_year', 'work_type']).size().unstack(fill_value=0)
# ensure ordered columns exist (missing ones get filled with 0)
cols = ['On-site (0%)', 'Hybrid (50%)', 'Remote (100%)']
flow_remote = flow_remote.reindex(columns=cols, fill_value=0)
flow_remote_perc = flow_remote.div(flow_remote.sum(axis=1).replace(0, 1), axis=0) * 100

colors_flow_remote = ['#FC6E51', '#F6BB42', '#3BAFDA']
ax1.stackplot(flow_remote_perc.index, 
             flow_remote_perc['On-site (0%)'], flow_remote_perc['Hybrid (50%)'], flow_remote_perc['Remote (100%)'], 
             labels=['Văn phòng (0% Remote)', 'Hybrid (50% Remote)', 'Từ xa (100% Remote)'],
             colors=colors_flow_remote, alpha=0.85)

ax1.set_xlabel('Năm làm việc', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_ylabel('Tỷ trọng hình thức làm việc (%)', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_title('A. Sự dịch chuyển hình thức làm việc (Remote)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xticks(flow_remote_perc.index)
ax1.set_ylim(0, 100)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x)}%"))
ax1.grid(True, linestyle='--', alpha=0.25)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(loc='lower left', title='Hình thức làm việc')

# Subplot 2: Experience Levels shift over years
flow_exp = df.groupby(['work_year', 'experience_level']).size().unstack(fill_value=0)
flow_exp = flow_exp[exp_order]
flow_exp_perc = flow_exp.div(flow_exp.sum(axis=1), axis=0) * 100

colors_flow_exp = [COLORS_EXP[exp] for exp in exp_order]
ax2.stackplot(flow_exp_perc.index,
             flow_exp_perc['EN'], flow_exp_perc['MI'], flow_exp_perc['SE'], flow_exp_perc['EX'],
             labels=['Entry-level (EN)', 'Mid-level (MI)', 'Senior-level (SE)', 'Executive (EX)'],
             colors=colors_flow_exp, alpha=0.85)

ax2.set_xlabel('Năm làm việc', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_ylabel('Tỷ trọng cấp bậc nhân sự (%)', fontsize=11, fontweight='bold', labelpad=8)
ax2.set_title('B. Dòng chảy dịch chuyển cơ cấu kinh nghiệm thị trường', fontsize=12, fontweight='bold', pad=12)
ax2.set_xticks(flow_exp_perc.index)
ax2.set_ylim(0, 100)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x)}%"))
ax2.grid(True, linestyle='--', alpha=0.25)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='lower left', title='Cấp bậc kinh nghiệm')

fig.suptitle('5. Flow: Phân tích dòng chảy & Chuyển dịch cơ cấu ngành công nghệ (2020 - 2024)', fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
flow_path = os.path.join(CHARTS_DIR, "5_flow.png")
plt.savefig(flow_path, dpi=300)
plt.close()
print(f"-> Saved: {flow_path}")

print("Refined visualization run complete. All 5 advanced multi-panel charts saved successfully.")

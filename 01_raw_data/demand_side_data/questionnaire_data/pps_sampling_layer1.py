"""
兰州市四区基层调研 · 第一层 PPS 系统抽样程序
================================================
抽样方法依据：《完整双层PPS抽样思路》
街道数据来源：《兰州市四区60岁以上人口统计表.xlsx》

目标：
  从城关区、七里河区、西固区、安宁区中，依据各区60岁以上人口
  按 EPSEM（等概率入样）原则分配街道数 bk，在每个区内用 PPS
  系统抽样法抽取 bk 个街道/乡镇，共计 b = 10 个。

符号约定（与 Word 文档保持一致）：
  K      ：区的总数
  Mk     ：第 k 区60岁以上人口（区级参数，来自 Word 文档）
  M      ：四区60岁以上人口合计，M = Σ(k=1→K) Mk
  Mkj    ：第 k 区第 j 个街道的60岁以上人口（来自 Excel）
  CUMj   ：第 k 区前 j 个街道的累计规模度量
  bk     ：第 k 区抽取的街道数
  b      ：全部抽取的街道总数，b = Σ bk = 10
  Ik     ：第 k 区的抽样间隔，Ik = Mk / bk
  rk     ：第 k 区的随机起点，rk ~ Uniform(1, Ik)
  m      ：每个街道抽取的社区数（第二层，=2，本程序不涉及）
  n      ：每个社区截访的个体数（第四层，=25，本程序不涉及）
"""

import sys
import numpy as np
import pandas as pd


# ====================================================================
# ★  可修改参数区
#    每处标有 ← ★ 的均为可调整项，其余请勿随意修改
# ====================================================================

# ① 随机数种子
#    整数 → 固定种子，每次运行结果相同（便于复现）
#    None → 每次运行结果随机
RANDOM_SEED = 42                                     # ← ★ 可修改

# ② 数据文件路径（相对路径 或 绝对路径均可）
DATA_FILE = "兰州市四区60岁以上人口统计表.xlsx"      # ← ★ 可修改

# ③ 工作表名称（默认对应 Excel 中的"四区数据"工作表）
SHEET_NAME = "四区数据"                              # ← ★ 可修改

# ④ Excel 列名映射
#    若 Excel 表头名称发生变化，仅需在此处更新，程序其余部分无需改动
COL_DIST = "区"                  # 区的列名         ← ★ 可修改
COL_STR  = "乡镇街道"            # 街道/乡镇列名    ← ★ 可修改
COL_POP  = "六十岁以上人口数"    # 规模度量 Mkj     ← ★ 可修改


# ====================================================================
# ★  设计参数（来自 Word 文档符号说明表，符号与原文完全一致）
# ====================================================================

# K：区的总数（Word 符号说明表）
K = 4                                                # ← ★ 若调整区域范围可修改
                                                     #   需同步更新 district_names 和 M_k

# 各区名称（顺序对应 M1…MK，需与 Excel "区"列完全一致）
district_names = ["城关区", "七里河区", "西固区", "安宁区"]  # ← ★ 可修改

# Mk：各区60岁以上人口
#   来源：Word 文档"符号说明·已知数据"表
#   用途：EPSEM 原则下计算各区应抽街道数 bk
#   注意：该值与 Excel 街道级数据加总可能存在小幅差异（数据口径不同），
#         差异不影响 bk 分配；在区内 PPS 抽样时以 Excel 实际合计为准。
M_k = {                                              # ← ★ 若区级人口数据更新，在此修改
    "城关区":  354000,    # M1（Word 文档值）
    "七里河区": 122800,   # M2（Word 文档值）
    "西固区":   80300,    # M3（Word 文档值）
    "安宁区":   62600,    # M4（Word 文档值）
}

# M：四区60岁以上人口合计（Word 文档：M = Σ(k=1→K) Mk = 619700）
M = sum(M_k.values())                                # 由 M_k 自动计算，无需手动修改

# b：第一层共抽取街道/乡镇数（Word 核心逻辑：b = 10）
b = 10                                               # ← ★ 可修改；需满足 b×m×n = 总样本量

# m：每个街道抽取的社区数（Word：m = 2）
m = 2                                                # ← ★ 可修改；建议保持 m ≥ 2

# n：每个社区截访的个体数（Word：n = 25）
n = 25                                               # ← ★ 可修改；建议 20 ≤ n ≤ 35


# ====================================================================
# 函数 1：计算各区分配街道数 bk
# ====================================================================

def compute_bk(district_names, M_k, M, b):
    """
    按 EPSEM 原则分配各区应抽街道数 bk（Word 第三节）：
        bk* = b × Mk / M（精确值）
        bk  = round(bk*)（取整）

    若取整后 Σbk ≠ b，对余数绝对值最大的区进行补位调整，
    确保 Σbk = b。

    返回
    ----
    bk_star : dict  精确值 bk*
    bk_int  : dict  取整值 bk
    """
    bk_star = {k: b * M_k[k] / M for k in district_names}
    bk_int  = {k: round(v) for k, v in bk_star.items()}

    diff = b - sum(bk_int.values())
    if diff != 0:
        # 余数 = 精确值 - 取整值
        rem  = {k: bk_star[k] - bk_int[k] for k in district_names}
        # diff>0（总和偏小）→ 余数最大的区加1；diff<0 → 余数最小的区减1
        keys = sorted(rem, key=lambda k: rem[k], reverse=(diff > 0))
        for k in keys[:abs(diff)]:
            bk_int[k] += 1 if diff > 0 else -1

    assert sum(bk_int.values()) == b, \
        f"分配错误：Σbk = {sum(bk_int.values())}，应等于 b = {b}"
    return bk_star, bk_int


# ====================================================================
# 函数 2：PPS 系统抽样（单区）
# ====================================================================

def pps_systematic(district_df, bk_val, rng):
    """
    对单个区执行 PPS 系统抽样，抽取 bk_val 个街道/乡镇。

    算法步骤严格对应 Word 第四节：

    第一步  将所有街道排成一列，计算累计 MOS：
              CUMj = Σ(j'=1 → j) Mkj'
            最后一个街道的 CUMj 即为本区所有街道 Mkj 之和（记为 Mk_actual）。

    第二步  计算抽样间隔：
              Ik = Mk_actual / bk
            （此处以 Excel 实际合计 Mk_actual 作为 Mk，
              保证 CUM[-1] == Mk，内部一致）

    第三步  在 [1, Ik] 内均匀随机抽取起点：
              rk ~ Uniform(1, Ik)

    第四步  生成 bk 个选择点：
              rk, rk + Ik, rk + 2·Ik, …, rk + (bk-1)·Ik

    第五步  各选择点对应"CUM 首次 ≥ 选择点"的街道即被选中
              （np.searchsorted side='left' 实现）

    参数
    ----
    district_df : pd.DataFrame  含 COL_STR、COL_POP 两列
    bk_val      : int           本区应抽街道数
    rng         : np.random.Generator

    返回
    ----
    dict：selected（抽中街道名列表）、r_k（随机起点）、I_k（抽样间隔）、
          Mk_actual（Excel 实际合计）、sel_pts（选择点列表）、
          sel_idx（被选中街道的行下标）、detail（含累计表的 DataFrame）
    """
    data  = district_df[[COL_STR, COL_POP]].reset_index(drop=True)
    Mkj   = data[COL_POP].values.astype(float)
    names = data[COL_STR].values

    # 第一步：累计 MOS
    CUM        = np.cumsum(Mkj)          # CUMj，共 Jk 个值
    Mk_actual  = float(CUM[-1])          # Mk（Excel 实际合计）

    # 第二步：抽样间隔 Ik = Mk / bk
    I_k = Mk_actual / bk_val

    # 第三步：随机起点 rk ~ Uniform(1, Ik)
    r_k = float(rng.uniform(1, I_k))

    # 第四步：bk 个选择点
    sel_pts = [r_k + i * I_k for i in range(bk_val)]

    # 第五步：各选择点 → 累计 MOS 首次 ≥ 选择点的街道下标
    sel_idx  = [
        min(int(np.searchsorted(CUM, sp, side="left")), len(names) - 1)
        for sp in sel_pts
    ]
    selected = [names[i] for i in sel_idx]

    # 构建详情表（含累计 MOS 和是否选中标记，用于输出核验）
    detail             = data.copy()
    detail["CUMj"]     = CUM
    detail["is_sel"]   = ["✓" if i in sel_idx else "" for i in range(len(names))]

    return dict(
        selected   = selected,
        r_k        = r_k,
        I_k        = I_k,
        Mk_actual  = Mk_actual,
        sel_pts    = sel_pts,
        sel_idx    = sel_idx,
        detail     = detail,
    )


# ====================================================================
# 主程序
# ====================================================================

def main():

    # ── 加载 Excel 数据 ──────────────────────────────────────────────
    # header=1：Excel 第1行为标题行（大表头），第2行才是列名
    HEADER_ROW = 1                                   # ← ★ 可修改（0-based，0表示第1行为列名）
    try:
        df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME,
                           header=HEADER_ROW, engine="openpyxl")
    except FileNotFoundError:
        sys.exit(f"[错误] 找不到数据文件：{DATA_FILE}\n"
                 f"       请将 Excel 文件放置在脚本同目录，或修改 DATA_FILE 路径。")

    df.columns  = df.columns.str.strip()
    df[COL_POP] = pd.to_numeric(df[COL_POP], errors="coerce")

    # ── 计算各区 bk ──────────────────────────────────────────────────
    bk_star, bk_int = compute_bk(district_names, M_k, M, b)

    # ── 初始化随机数生成器 ───────────────────────────────────────────
    rng = np.random.default_rng(RANDOM_SEED)

    # ── 打印总览 ─────────────────────────────────────────────────────
    SEP = "═" * 72
    sep = "─" * 72
    print(SEP)
    print("   第一层 PPS 系统抽样  ·  兰州市四区基层调研")
    print(SEP)
    print(f"   K={K}  b={b}  m={m}  n={n}  "
          f"总样本量 b×m×n = {b}×{m}×{n} = {b*m*n}")
    print(f"   四区60岁以上人口合计  M = {M:,}（来自 Word 文档）")
    print(f"   随机数种子  RANDOM_SEED = {RANDOM_SEED}")
    print()
    print(f"   {'区':<10} {'Mk（文档）':>12} {'bk*（精确）':>13} {'bk（取整）':>10}")
    print(f"   {sep[:48]}")
    for k in district_names:
        print(f"   {k:<10} {M_k[k]:>12,} {bk_star[k]:>13.4f} {bk_int[k]:>10}")
    print(f"   {'合计':<10} {M:>12,} {'—':>13} {sum(bk_int.values()):>10}")
    print(SEP)

    all_results = []   # 收集全部抽中街道

    # ── 逐区 PPS 抽样 ─────────────────────────────────────────────────
    for k_name in district_names:
        bk_val = bk_int[k_name]
        sub_df = df[df[COL_DIST] == k_name].copy()

        if sub_df.empty:
            sys.exit(f"[错误] Excel 中找不到区名「{k_name}」，"
                     f"请检查 COL_DIST 列名或区名拼写。")

        res = pps_systematic(sub_df, bk_val, rng)

        # 打印本区抽样过程
        print(f"\n   ── {k_name}（bk = {bk_val}）{'─'*50}")
        print(f"   Mk（Word文档）= {M_k[k_name]:,}     "
              f"Mk（Excel合计）= {res['Mk_actual']:,.0f}")
        print(f"   抽样间隔  Ik = Mk / bk = {res['Mk_actual']:,.0f} / {bk_val}"
              f" = {res['I_k']:.2f}")
        print(f"   随机起点  rk ~ Uniform(1, {res['I_k']:.2f}) = {res['r_k']:.2f}")
        pts_str = "   ".join([f"pt{i+1}={p:.2f}" for i, p in enumerate(res['sel_pts'])])
        print(f"   选择点：{pts_str}")
        print()

        # 打印累计 MOS 表
        print(f"   {'j':>3}  {'街道 / 乡镇':<20}  {'Mkj':>9}  {'CUMj':>12}  {'选中'}")
        print(f"   {'─'*58}")
        for j, row in res["detail"].iterrows():
            flag = "  ← ✓ 选中" if row["is_sel"] == "✓" else ""
            print(f"   {j+1:>3}  {row[COL_STR]:<20}  "
                  f"{int(row[COL_POP]):>9,}  {int(row['CUMj']):>12,}{flag}")

        print()
        print(f"   ★ {k_name} 抽中街道/乡镇（共 {bk_val} 个）：")
        for i, s in enumerate(res["selected"], 1):
            mkj = int(sub_df.loc[sub_df[COL_STR] == s, COL_POP].values[0])
            print(f"      {i}. {s}（Mkj = {mkj:,}）")

        for s in res["selected"]:
            all_results.append({"区": k_name, "街道/乡镇": s})

    # ── 汇总输出 ──────────────────────────────────────────────────────
    print(f"\n{SEP}")
    print("   ★★  第一层抽样汇总：共 10 个街道 / 乡镇  ★★")
    print(SEP)
    for i, row in enumerate(all_results, 1):
        print(f"   {i:>2}. {row['区']:<10}  {row['街道/乡镇']}")
    print(SEP)
    print(f"   验证：实际抽中 {len(all_results)} 个（应 = b = {b}）")
    print(f"   预期调查样本量 = {len(all_results)} × {m} × {n} = "
          f"{len(all_results) * m * n} 人")
    print(SEP)


if __name__ == "__main__":
    main()

MWTDS-CPLEX Experimental Toolkit
Graph Format Conversion + CPLEX Exact Solver Framework
图格式转换与 CPLEX 精确求解实验框架
1. Project Overview ｜项目简介
English

This repository provides a lightweight experimental framework for solving the Minimum Weight Total Dominating Set (MWTDS) problem using CPLEX.

The project includes:

Graph format conversion scripts

CPLEX Python exact solvers

OPL single-run model

Batch experiment scripts

Structured result output

It supports reproducible experiments on DIMACS, general graphs, and UDG graphs.

中文

本仓库提供一个基于 CPLEX 的 最小加权全支配集（MWTDS） 精确求解实验框架，包含：

多种图格式转换脚本

CPLEX Python 精确求解程序

OPL 单次求解模型

批量实验流程

结构化结果输出

支持 DIMACS、general 图、UDG 图等多种实例格式。

2. Repository Structure ｜目录结构说明
cplex_graph_dimacs1/         # DIMACS 转换后的图数据
cplex_graph_dimacs2/

cplex_graph_t_weight/        # 带权 general 图数据
cplex_graph_udg_weight/      # 带权 UDG 图数据

results/                     # 批量实验结果输出目录

cplex.txt                    # OPL 数据示例

dimacs_to_cplexdat.py        # DIMACS → CPLEX .dat 转换
dimacs2_to_cplexdat.py       # DIMACS 变体转换

general_to_cplex_weight.py   # general 图 → CPLEX (带权)
udg_to_cplex_weight.py       # UDG 图 → CPLEX (带权)
udg_to_cplexdat.py           # UDG → CPLEX (无权结构)

wtds_cplex.py                # 无权实例 CPLEX 批量实验
wtds_cplex_weight.py         # general 带权实例求解
wtds_udg_cplex_weight.py     # UDG 带权实例求解
3. Supported Input Types ｜支持的图类型
3.1 DIMACS Graphs (Unweighted)

转换后 .txt/.dat 文件仅包含：

V_num

Edges

权重在 CPLEX Python 求解脚本中生成：

weight(i) = (i % 200) + 1

（顶点编号从 1 开始）

3.2 General Graph (Weighted)

输入文件包含顶点权重

转换脚本读取并写入：

weight = [w1, w2, ..., wn];

CPLEX 模型直接使用该权重

3.3 UDG Graph (Weighted)

读取文件自带权重

写入 .dat

Python 模型读取权重数组作为目标函数系数

4. CPLEX Models ｜CPLEX 求解模型
4.1 Python-based Exact Solver

文件：

wtds_cplex.py（无权）

wtds_cplex_weight.py（general）

wtds_udg_cplex_weight.py（UDG）

模型特性：

二进制变量 x[i]

目标：最小化顶点权重之和

约束：每个顶点至少有一个邻居被选中（Total Dominating）

线程数固定为 1（保证结果稳定性）

4.2 OPL Single-run Model

使用 .mod + .dat

目标函数内置 (i % 200 + 1) 权重规则

适用于单实例精确求解

5. Batch Experiment Workflow ｜批量实验流程

Python 批量脚本功能：

读取指定目录下所有 .txt

解析 V_num, Edges, weight（如存在）

构建 CPLEX 模型

设置时间限制

求解

将结果追加写入 results/

输出格式示例：

instance1.txt: Total Dominating Vertices = 123, Solve Time = 5.2341 seconds
6. Runtime Environment ｜运行环境

Tested Environment:

OS: Windows / Ubuntu

Python: 3.8+

CPLEX: 22.1+

CPLEX Python API installed

tqdm

Install dependencies:

pip install tqdm

CPLEX Python API must be installed separately.

7. How to Run ｜使用方法
7.1 Convert Graph Format

Example:

python dimacs_to_cplexdat.py
python general_to_cplex_weight.py
7.2 Run Batch Exact Solver

Example:

python wtds_cplex.py
python wtds_cplex_weight.py
python wtds_udg_cplex_weight.py

Results will be written into:

results/
8. Problem Type ｜问题类型

This framework solves:

Minimum Weight Total Dominating Set (MWTDS)

Each vertex must be dominated by at least one neighbor.

Self-domination is not allowed.

9. Author ｜作者

Wenlong You
M.S. in Computer Science

Research Areas:

Combinatorial Optimization

Exact & Heuristic Methods

Graph Algorithms

Local Search
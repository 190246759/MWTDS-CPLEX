import os
import re
import time  # 导入时间模块
from cplex import Cplex
from cplex.exceptions import CplexError
from tqdm import tqdm

# 读取并解析图信息
def read_graph_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # 提取 V_num
    v_num_match = re.search(r"V_num\s*=\s*(\d+);", content)
    if v_num_match:
        V_num = int(v_num_match.group(1))
    else:
        raise ValueError("V_num not found in the file.")

    # 提取边集
    edges_match = re.search(r"Edges\s*=\s*\{([^}]*)\};", content)
    if edges_match:
        edges_str = edges_match.group(1)
        edges = [tuple(map(int, edge.strip("<>, ").split(","))) for edge in edges_str.split("\n") if edge.strip()]
    else:
        raise ValueError("Edges not found in the file.")

    return V_num, edges

# 使用 CPLEX 求解最小支配集问题
def solve_dominating_set(V_num, edges):
    model = Cplex()
    model.objective.set_sense(model.objective.sense.minimize)
    model.set_problem_type(Cplex.problem_type.LP)
    model.parameters.threads.set(1)  # 设置线程数为1
    model.set_log_stream(None)  # 关闭日志输出
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    # 添加决策变量 x[i]
    x = {i: f"x_{i}" for i in range(1, V_num + 1)}
    model.variables.add(names=list(x.values()), types=["B"] * V_num)

    # 添加目标函数：最小化总权重 (i % 200 + 1) * x[i]
    obj_coeffs = [(x[i], (i % 200 + 1)) for i in range(1, V_num + 1)]
    model.objective.set_linear(obj_coeffs)

    # 添加约束条件：每个顶点必须至少有一个邻居在支配集中
    for i in range(1, V_num + 1):
        neighbors = [j for (j, k) in edges if k == i] + [j for (k, j) in edges if k == i]
        neighbor_vars = [x[j] for j in neighbors]
        if neighbor_vars:  # 确保有邻居
            model.linear_constraints.add(
                lin_expr=[(neighbor_vars, [1.0] * len(neighbor_vars))],
                senses=["G"],
                rhs=[1.0]
            )

    # 求解模型
    try:
        start_time = time.time()  # 记录求解开始时间
        model.solve()
        end_time = time.time()  # 记录求解结束时间
        total_dominating_vertices = model.solution.get_objective_value()
        solve_time = end_time - start_time  # 计算求解时间
        return total_dominating_vertices, solve_time
    except CplexError as exc:
        return None, None

# 主程序
if __name__ == "__main__":
    folder_path = "C:/Users/GodAeolus/Desktop/cplex_python/cplex_graph_t"  # 文件夹路径
    output_txt_file = "C:/Users/GodAeolus/Desktop/cplex_python/results/results_t.txt"  # 输出的 txt 文件名

    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # 遍历每个文件并求解，添加进度条
    for file_name in tqdm(files, desc="Processing files", unit="file"):
        file_path = os.path.join(folder_path, file_name)

        try:
            V_num, edges = read_graph_from_file(file_path)
            total_dominating_vertices, solve_time = solve_dominating_set(V_num, edges)
            if total_dominating_vertices is not None:
                # 动态写入结果到 txt 文件
                with open(output_txt_file, "a") as output_file:  # 使用追加模式
                    output_file.write(f"{file_name}: Total Dominating Vertices = {total_dominating_vertices}, Solve Time = {solve_time:.4f} seconds\n")
                print(f"Processed: {file_name} - Total Dominating Vertices: {total_dominating_vertices}, Solve Time: {solve_time:.4f} seconds")
            else:
                with open(output_txt_file, "a") as output_file:  # 使用追加模式
                    output_file.write(f"{file_name}: Error in solving the problem\n")
                print(f"Error processing {file_name}: Unable to solve the problem")
        except Exception as e:
            tqdm.write(f"Error processing file {file_name}: {e}")
            with open(output_txt_file, "a") as output_file:  # 使用追加模式
                output_file.write(f"{file_name}: Error - {str(e)}\n")

    print(f"Results have been written to {output_txt_file}")
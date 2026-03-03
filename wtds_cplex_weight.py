import os
import re
import time
from cplex import Cplex
from cplex.exceptions import CplexError
from tqdm import tqdm

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

    # 提取权重数组
    weight_match = re.search(r"weight\s*=\s*\[([^\]]*)\];", content)
    if weight_match:
        weight_str = weight_match.group(1).replace(" ", "")  # 去除多余空格
        weight = list(map(int, weight_str.split(",")))
    else:
        raise ValueError("Weight array not found in the file.")

    if len(weight) != V_num:
        raise ValueError(f"Weight array length ({len(weight)}) does not match V_num ({V_num}).")

    return V_num, edges, weight

def solve_dominating_set(V_num, edges, weight, time_limit=3600):
    model = Cplex()
    model.objective.set_sense(model.objective.sense.minimize)
    model.set_problem_type(Cplex.problem_type.LP)
    model.parameters.threads.set(1)
    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    # 设置时间限制
    model.parameters.timelimit.set(time_limit)

    x = {i: f"x_{i}" for i in range(1, V_num + 1)}
    model.variables.add(names=list(x.values()), types=["B"] * V_num)

    obj_coeffs = [(x[i], weight[i - 1]) for i in range(1, V_num + 1)]
    model.objective.set_linear(obj_coeffs)

    for i in range(1, V_num + 1):
        neighbors = [j for (j, k) in edges if k == i] + [j for (k, j) in edges if k == i]
        neighbor_vars = [x[j] for j in neighbors]
        if neighbor_vars:
            model.linear_constraints.add(
                lin_expr=[(neighbor_vars, [1.0] * len(neighbor_vars))],
                senses=["G"],
                rhs=[1.0]
            )
        else:
            print(f"Warning: Vertex {i} has no neighbors.")

    try:
        start_time = time.time()
        model.solve()
        end_time = time.time()
        total_dominating_vertices = model.solution.get_objective_value()
        solve_time = end_time - start_time
        print(f"Solution status: {model.solution.get_status()}")
        return total_dominating_vertices, solve_time
    except CplexError as exc:
        print(f"Cplex Error: {exc}")
        return None, None

if __name__ == "__main__":
    folder_path = "C:/Users/GodAeolus/Desktop/cplex_python/cplex_graph_t_weight_2"
    output_txt_file = "C:/Users/GodAeolus/Desktop/cplex_python/results/results_t_weight_2.txt"

    os.makedirs(os.path.dirname(output_txt_file), exist_ok=True)

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    for file_name in tqdm(files, desc="Processing files", unit="file"):
        file_path = os.path.join(folder_path, file_name)

        try:
            V_num, edges, weight = read_graph_from_file(file_path)
            total_dominating_vertices, solve_time = solve_dominating_set(V_num, edges, weight, time_limit=3600)
            if total_dominating_vertices is not None:
                with open(output_txt_file, "a") as output_file:
                    output_file.write(f"{file_name}: Total Dominating Vertices = {total_dominating_vertices}, Solve Time = {solve_time:.4f} seconds\n")
                print(f"Processed: {file_name} - Total Dominating Vertices: {total_dominating_vertices}, Solve Time: {solve_time:.4f} seconds")
            else:
                with open(output_txt_file, "a") as output_file:
                    output_file.write(f"{file_name}: Error in solving the problem\n")
                print(f"Error processing {file_name}: Unable to solve the problem")
        except Exception as e:
            tqdm.write(f"Error processing file {file_name}: {e}")
            with open(output_txt_file, "a") as output_file:
                output_file.write(f"{file_name}: Error - {str(e)}\n")

    print(f"Results have been written to {output_txt_file}")
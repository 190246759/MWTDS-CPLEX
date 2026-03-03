import os

def read_graph(filename):
    edges = []  # 在读取行之前初始化边列表
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("p edge"):
                V_num, E_num = map(int, line.split()[2:])
            elif line.startswith("e"):
                _, v1, v2 = line.split()
                edges.append((int(v1), int(v2)))
    return V_num, edges

def write_graph(filename, V_num, edges):
    with open(filename, 'w') as file:
        file.write(f"V_num = {V_num};\n")
        file.write("Edges = {\n")
        for edge in edges:
            file.write(f"<{edge[0]},{edge[1]}>,\n")
        file.write("};")

input_folder = "C:/Users/GodAeolus/Desktop/cplex_python/dimacs2"
output_folder = "C:/Users/GodAeolus/Desktop/cplex_python/cplex_graph_dimacs2"

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取输入文件夹中所有的 .mis 文件
mis_files = [f for f in os.listdir(input_folder) if f.endswith('.mis')]

# 按顺序处理每个 .mis 文件
for mis_file in mis_files:
    input_filename = os.path.join(input_folder, mis_file)
    output_filename = os.path.join(output_folder, mis_file.replace('.mis', '.txt'))  # 将扩展名替换为 .txt

    V_num, edges = read_graph(input_filename)
    write_graph(output_filename, V_num, edges)

    # 确保 V_num 和 edges 被正确读取
    print("已处理文件:", mis_file)
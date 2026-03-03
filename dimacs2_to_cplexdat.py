import os

def read_graph(filename):
    V_num = None
    edges = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("p e"):
                _, _, V_num, E_num = line.split()
                V_num = int(V_num)
                E_num = int(E_num)
            elif line.startswith("e"):
                _, v1, v2 = line.split()
                edges.append((int(v1), int(v2)))
    
    if V_num is None:
        raise ValueError(f"File {filename} does not contain a valid 'p e' line.")
    
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

    try:
        V_num, edges = read_graph(input_filename)
        write_graph(output_filename, V_num, edges)
        print("已处理文件:", mis_file)
    except Exception as e:
        print(f"处理文件 {mis_file} 时出错: {e}")
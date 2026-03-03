import os

def convert_format(input_folder, output_folder):
    try:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 获取输入文件夹中的所有文件
        files = [f for f in os.listdir(input_folder) if f.startswith("Problem.dat_")]

        # 遍历每个文件并进行转换
        for file_name in files:
            input_file = os.path.join(input_folder, file_name)
            # 生成输出文件名，直接在原始文件名后添加 .txt 后缀
            output_file = os.path.join(output_folder, f"{file_name}.txt")

            with open(input_file, 'r') as file:
                lines = file.readlines()

            # 检查文件是否为空
            if not lines:
                print(f"警告：文件 {file_name} 为空，跳过处理。")
                continue

            # 提取节点数量
            if "NumberOfNodes:" not in lines[0].strip():
                print(f"警告：文件 {file_name} 格式错误，跳过处理。")
                continue
            try:
                num_nodes = int(lines[1].strip())  # 节点数量在第二行
            except ValueError:
                print(f"警告：文件 {file_name} 格式错误，无法提取节点数量，跳过处理。")
                continue

            # 提取权重
            weights_start = None
            for i, line in enumerate(lines):
                if "******************WEIGHTS*****************************" in line:
                    weights_start = i + 1
                    break
            if weights_start is None:
                print(f"警告：文件 {file_name} 格式错误，未找到 'WEIGHTS' 标记，跳过处理。")
                continue

            try:
                weights = [int(lines[weights_start + i].strip()) for i in range(num_nodes)]
            except ValueError:
                print(f"警告：文件 {file_name} 权重格式错误，跳过处理。")
                continue

            # 查找连接矩阵的起始位置
            connections_start = None
            for i, line in enumerate(lines):
                if "*****************CONNECTIONS****************" in line:
                    connections_start = i + 1
                    break
            if connections_start is None:
                print(f"警告：文件 {file_name} 格式错误，未找到 'CONNECTIONS' 标记，跳过处理。")
                continue

            # 提取连接矩阵部分
            connections = []
            for line in lines[connections_start:connections_start + num_nodes]:
                try:
                    row = [int(x) for x in line.strip().split()]
                    if len(row) != num_nodes:
                        print(f"警告：文件 {file_name} 连接矩阵格式错误，某一行的列数不等于节点数量 {num_nodes}，跳过处理。")
                        break
                    connections.append(row)
                except ValueError:
                    print(f"警告：文件 {file_name} 连接矩阵格式错误，某一行包含非数字字符，跳过处理。")
                    break
            else:
                # 转换为边的格式
                edges = []
                for i in range(num_nodes):
                    for j in range(i + 1, num_nodes):
                        if connections[i][j] == 1:
                            edges.append(f"<{i + 1},{j + 1}>")

                # 构建输出字符串
                output = f"V_num = {num_nodes};\n"
                output += "Edges = {\n"
                output += ",\n".join(edges)
                output += "\n};\n"
                output += f"weight = [{','.join(map(str, weights))}];"  # 权重数组中没有空格

                # 保存到新的文件
                with open(output_file, 'w') as outfile:
                    outfile.write(output)

                print(f"文件 {file_name} 转换完成，结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"错误：文件夹 {input_folder} 未找到。")
    except Exception as e:
        print(f"未知错误：{e}")

# 指定输入和输出文件夹路径
input_folder = "C:/Users/GodAeolus/Desktop/cplex_python/t"  # 输入文件夹路径
output_folder = "C:/Users/GodAeolus/Desktop/cplex_python/cplex_graph_t_weight"  # 输出文件夹路径

# 调用函数进行批量转换
convert_format(input_folder, output_folder)
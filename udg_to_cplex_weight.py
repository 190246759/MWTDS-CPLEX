import os

def convert_format(input_folder, output_folder):
    try:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 获取输入文件夹中的所有文件
        files = [f for f in os.listdir(input_folder) if f.startswith("graph")]

        # 遍历每个文件并进行转换
        for file_name in files:
            input_file = os.path.join(input_folder, file_name)
            # 输出文件名直接在原始文件名后添加 .txt 后缀
            output_file = os.path.join(output_folder, f"{file_name}.txt")

            with open(input_file, 'r') as file:
                lines = file.readlines()

            # 检查文件是否为空
            if not lines:
                print(f"警告：文件 {file_name} 为空，跳过处理。")
                continue

            # 提取顶点数量
            try:
                num_nodes = int(lines[0].strip())  # 顶点数量在第一行
            except ValueError:
                print(f"警告：文件 {file_name} 格式错误，无法提取顶点数量，跳过处理。")
                continue

            # 提取权重数组（权重数组在顶点数量之后）
            try:
                weights = [int(line.strip().split()[1]) for line in lines[1:num_nodes + 1]]
            except ValueError:
                print(f"警告：文件 {file_name} 权重数组格式错误，跳过处理。")
                continue

            # 找到边信息的起始位置（权重数组之后有一个空行）
            edges_start = None
            for i, line in enumerate(lines[num_nodes + 1:], start=num_nodes + 1):
                if line.strip() == "":
                    edges_start = i + 1
                    break
            if edges_start is None:
                print(f"警告：文件 {file_name} 格式错误，未找到边信息的起始位置，跳过处理。")
                continue

            # 提取边信息并去重
            edges = set()  # 使用集合存储边，自动去重
            for line in lines[edges_start:]:
                try:
                    u, v = map(int, line.strip().split())
                    # 确保边是无向的，存储为 (min(u, v), max(u, v))
                    edge = (min(u, v), max(u, v))
                    edges.add(edge)
                except ValueError:
                    print(f"警告：文件 {file_name} 边信息格式错误，跳过处理。")
                    break
            else:
                # 将边的集合转换为列表并排序
                # 自定义排序：先按起始顶点排序，如果起始顶点相同，则按终止顶点排序
                edges = sorted(list(edges), key=lambda x: (x[0], x[1]))

                # 构建输出字符串
                output = f"V_num = {num_nodes};\n"
                output += "Edges = {\n"
                output += ",\n".join([f"<{u + 1},{v + 1}>" for u, v in edges])  # 顶点编号从0开始，需要加1
                output += "\n};\n"
                output += f"weight = [{','.join(map(str, weights))}];"

                # 保存到新的文件
                with open(output_file, 'w') as outfile:
                    outfile.write(output)

                print(f"文件 {file_name} 转换完成，结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"错误：文件夹 {input_folder} 未找到。")
    except Exception as e:
        print(f"未知错误：{e}")

# 指定输入和输出文件夹路径
input_folder = "C:/Users/GodAeolus/Desktop/cplex_python/udg"  # 输入文件夹路径
output_folder = "C:/Users/GodAeolus/Desktop/cplex_python/cplex_graph_udg_weight"  # 输出文件夹路径

# 调用函数进行批量转换
convert_format(input_folder, output_folder)
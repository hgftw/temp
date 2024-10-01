import os

# 设置文件夹路径
folder_path = 'trainingdata2/valid/combine'

# 获取文件夹中的所有文件
files = os.listdir(folder_path)

# 筛选出所有png和txt文件
png_files = [f for f in files if f.endswith('.png')]
txt_files = [f for f in files if f.endswith('.txt')]

# 检查并删除空的txt文件及其对应的png文件
for txt_file in txt_files:
    # 构建对应的png文件名
    png_file = txt_file.replace('.txt', '.png')
    
    # 检查是否存在对应的png文件
    if png_file in png_files:
        txt_file_path = os.path.join(folder_path, txt_file)
        png_file_path = os.path.join(folder_path, png_file)
        
        # 检查txt文件是否为空
        if os.path.getsize(txt_file_path) == 0:
            # 删除txt文件和对应的png文件
            os.remove(txt_file_path)
            os.remove(png_file_path)
            print(f"已删除空的txt文件: {txt_file} 和对应的图片: {png_file}")

print("处理完成")

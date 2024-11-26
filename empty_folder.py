import os
import shutil

# 指定要清空的文件夹路径
# folder_path = "指定文件夹路径"
# 调用函数清空文件夹
# empty_folder(folder_path)
def empty_folder(folder_path):
    # 确保文件夹存在
    if not os.path.exists(folder_path):
        print("文件夹不存在")
        return

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 删除文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"已删除文件: {file_path}")

        # 删除子文件夹
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)
            print(f"已删除文件夹: {dir_path}")

    print("文件夹已清空")



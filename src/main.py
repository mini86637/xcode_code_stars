import os
from utils.file_counter import cloc_stat_in_dirs

def find_pods_dir(project_path):
    """查找Pods目录路径"""
    for root, dirs, files in os.walk(project_path):
        if 'Pods' in dirs:
            return os.path.join(root, 'Pods')
    return None

def collect_main_second_level_folders(project_path, pods_dir):
    """收集主项目所有二级目录（不含Pods）"""
    second_level_folders = []
    for name in os.listdir(project_path):
        abs_path = os.path.join(project_path, name)
        if name == 'Pods' or not os.path.isdir(abs_path):
            continue
        # 一级目录本身也统计
        second_level_folders.append(abs_path)
        # 统计二级目录
        for subname in os.listdir(abs_path):
            sub_abs_path = os.path.join(abs_path, subname)
            if os.path.isdir(sub_abs_path):
                second_level_folders.append(sub_abs_path)
    return second_level_folders

def collect_pod_libs(pods_dir):
    """收集Pods下每个三方库一级目录"""
    pod_libs = []
    if pods_dir and os.path.isdir(pods_dir):
        for name in os.listdir(pods_dir):
            abs_path = os.path.join(pods_dir, name)
            if os.path.isdir(abs_path):
                pod_libs.append(abs_path)
    return pod_libs



if __name__ == "__main__":
    xcode_project_path = input("请输入Xcode项目的路径: ").strip()
    if not os.path.isdir(xcode_project_path):
        print("提供的路径无效，请检查后重试。")
        exit(1)

    pods_dir = find_pods_dir(xcode_project_path)
    main_folders = collect_main_second_level_folders(xcode_project_path, pods_dir)
    pod_libs = collect_pod_libs(pods_dir)

    code_exts = ['.swift', '.m', '.mm', '.h', '.c', '.cpp', '.py', '.java', '.js', '.ts']

    def print_stats(title, stats):
        print(f"\n===== {title} =====")
        print(f"类型    文件数  总行数  空行  注释行  代码行")
        total_files = total_lines = total_blank = total_comment = total_code = 0
        for ext, s in stats.items():
            if s['files'] == 0:
                continue
            print(f"{ext:<7} {s['files']:<6} {s['lines']:<6} {s['blank']:<5} {s['comment']:<7} {s['code']:<6}")
            total_files += s['files']
            total_lines += s['lines']
            total_blank += s['blank']
            total_comment += s['comment']
            total_code += s['code']
        print(f"合计   {total_files:<6} {total_lines:<6} {total_blank:<5} {total_comment:<7} {total_code:<6}")
        return total_code

    print("\n===== 主项目各一级目录统计 =====")
    main_total = 0
    for folder in main_folders:
        stats = cloc_stat_in_dirs([folder], code_exts)
        code = print_stats(os.path.basename(folder), stats)
        main_total += code

    print("\n===== Pod（三方库）各库统计 =====")
    pod_total = 0
    for pod in pod_libs:
        stats = cloc_stat_in_dirs([pod], code_exts)
        code = print_stats(os.path.basename(pod), stats)
        pod_total += code

    total_code = main_total + pod_total
    print("\n===== 占比 =====")
    if total_code > 0:
        print(f"主项目占比: {main_total/total_code:.2%}")
        print(f"Pod（三方库）占比: {pod_total/total_code:.2%}")
    else:
        print("未检测到代码行数")
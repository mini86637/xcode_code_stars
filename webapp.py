import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from src.utils.file_counter import cloc_stat_in_dirs
from src.main import find_pods_dir, collect_main_second_level_folders, collect_pod_libs

app = Flask(__name__)
app.secret_key = 'xcodecodestats2025'

CODE_EXTS = ['.swift', '.m', '.mm', '.h', '.c', '.cpp', '.py', '.java', '.js', '.ts']

def get_stats(project_path):
    pods_dir = find_pods_dir(project_path)
    main_folders = collect_main_second_level_folders(project_path, pods_dir)
    pod_libs = collect_pod_libs(pods_dir)
    main_results = []
    pod_results = []
    main_total = 0
    pod_total = 0
    for folder in main_folders:
        rel_path = os.path.relpath(folder, project_path)
        stats = cloc_stat_in_dirs([folder], CODE_EXTS)
        code = sum(s['code'] for s in stats.values())
        main_results.append({'name': os.path.basename(folder), 'rel_path': rel_path, 'stats': stats, 'code': code})
        main_total += code
    for pod in pod_libs:
        stats = cloc_stat_in_dirs([pod], CODE_EXTS)
        code = sum(s['code'] for s in stats.values())
        pod_results.append({'name': os.path.basename(pod), 'stats': stats, 'code': code})
        pod_total += code
    total_code = main_total + pod_total
    return main_results, pod_results, main_total, pod_total, total_code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_path = request.form.get('project_path', '').strip()
        if not os.path.isdir(project_path):
            flash('提供的路径无效，请检查后重试。')
            return redirect(url_for('index'))
        main_results, pod_results, main_total, pod_total, total_code = get_stats(project_path)
        return render_template('result.html', project_path=project_path,
                               main_results=main_results, pod_results=pod_results,
                               main_total=main_total, pod_total=pod_total, total_code=total_code)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

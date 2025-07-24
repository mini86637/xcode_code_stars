import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from src.utils.file_counter import cloc_stat_in_dirs
from src.main import find_pods_dir, collect_main_second_level_folders, collect_pod_libs

app = Flask(__name__)
app.secret_key = 'xcodecodestats2025'


CODE_EXTS = ['.swift', '.m', '.mm', '.h', '.c', '.cpp', '.py', '.java', '.js', '.ts']

LANGUAGES = [
    ('zh_cn', '简体中文'),
    ('zh_tw', '繁體中文'),
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('fr', 'Français'),
    ('hi', 'हिन्दी')
]

def load_lang(lang_code):
    with open('lang.json', 'r', encoding='utf-8') as f:
        langs = json.load(f)
    return langs.get(lang_code, langs['en'])

def get_stats(project_path, sort_key='code', reverse=True):
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
        file_count = sum(s['files'] for s in stats.values())
        total_lines = sum(s['lines'] for s in stats.values())
        blank = sum(s['blank'] for s in stats.values())
        comment = sum(s['comment'] for s in stats.values())
        main_results.append({
            'name': os.path.basename(folder),
            'rel_path': rel_path,
            'stats': stats,
            'code': code,
            'file_count': file_count,
            'total_lines': total_lines,
            'blank': blank,
            'comment': comment
        })
        main_total += code
    # Pod库聚合统计
    pod_stat_map = {}
    for pod in pod_libs:
        pod_name = os.path.basename(pod)
        stats = cloc_stat_in_dirs([pod], CODE_EXTS)
        if pod_name not in pod_stat_map:
            pod_stat_map[pod_name] = {
                'name': pod_name,
                'code': 0,
                'file_count': 0,
                'total_lines': 0,
                'blank': 0,
                'comment': 0,
                'stats': {}
            }
        pod_stat_map[pod_name]['code'] += sum(s['code'] for s in stats.values())
        pod_stat_map[pod_name]['file_count'] += sum(s['files'] for s in stats.values())
        pod_stat_map[pod_name]['total_lines'] += sum(s['lines'] for s in stats.values())
        pod_stat_map[pod_name]['blank'] += sum(s['blank'] for s in stats.values())
        pod_stat_map[pod_name]['comment'] += sum(s['comment'] for s in stats.values())
        # 合并stats类型
        for ext, s in stats.items():
            if ext not in pod_stat_map[pod_name]['stats']:
                pod_stat_map[pod_name]['stats'][ext] = {'files': 0, 'lines': 0, 'blank': 0, 'comment': 0, 'code': 0}
            pod_stat_map[pod_name]['stats'][ext]['files'] += s['files']
            pod_stat_map[pod_name]['stats'][ext]['lines'] += s['lines']
            pod_stat_map[pod_name]['stats'][ext]['blank'] += s['blank']
            pod_stat_map[pod_name]['stats'][ext]['comment'] += s['comment']
            pod_stat_map[pod_name]['stats'][ext]['code'] += s['code']
    pod_results = list(pod_stat_map.values())
    pod_total = sum(p['code'] for p in pod_results)
    # 排序
    main_results = sorted(main_results, key=lambda x: x.get(sort_key, 0), reverse=reverse)
    pod_results = sorted(pod_results, key=lambda x: x.get(sort_key, 0), reverse=reverse)
    total_code = main_total + pod_total
    return main_results, pod_results, main_total, pod_total, total_code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'lang' in request.form:
            session['lang'] = request.form.get('lang', 'zh_cn')
        lang = session.get('lang', 'zh_cn')
        texts = load_lang(lang)
        sort_key = request.form.get('sort_key', 'code')
        sort_order = request.form.get('sort_order', 'desc')
        reverse = sort_order == 'desc'
        sort_type = request.form.get('type', 'main')
        project_path = request.form.get('project_path', '').strip()
        if not os.path.isdir(project_path):
            flash(texts.get('invalid_path', '提供的路径无效，请检查后重试。'))
            return redirect(url_for('index'))
        # 始终获取全部数据，但只对主项目或三方库排序
        main_results, pod_results, main_total, pod_total, total_code = get_stats(project_path)
        if sort_type == 'main':
            main_results = sorted(main_results, key=lambda x: x.get(sort_key, 0), reverse=reverse)
        elif sort_type == 'pod':
            # pod_results聚合字段排序
            pod_results = sorted(pod_results, key=lambda x: x.get(sort_key, 0), reverse=reverse)
        return render_template('result.html', project_path=project_path,
                               main_results=main_results, pod_results=pod_results,
                               main_total=main_total, pod_total=pod_total, total_code=total_code,
                               texts=texts, lang=lang, languages=LANGUAGES,
                               sort_key=sort_key, sort_order=sort_order, sort_type=sort_type)
    else:
        lang = session.get('lang', 'zh_cn')
        texts = load_lang(lang)
        return render_template('index.html', texts=texts, lang=lang, languages=LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True)

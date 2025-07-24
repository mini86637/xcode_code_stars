import os
import re

COMMENT_SYNTAX = {
    '.swift': {'single': '//', 'multi': ('/*', '*/')},
    '.m': {'single': '//', 'multi': ('/*', '*/')},
    '.mm': {'single': '//', 'multi': ('/*', '*/')},
    '.h': {'single': '//', 'multi': ('/*', '*/')},
    '.c': {'single': '//', 'multi': ('/*', '*/')},
    '.cpp': {'single': '//', 'multi': ('/*', '*/')},
    '.py': {'single': '#'},
    '.java': {'single': '//', 'multi': ('/*', '*/')},
    '.js': {'single': '//', 'multi': ('/*', '*/')},
    '.ts': {'single': '//', 'multi': ('/*', '*/')},
}

def detect_comment(line, ext, in_multi_comment):
    syntax = COMMENT_SYNTAX.get(ext)
    if not syntax:
        return False, in_multi_comment
    line_strip = line.strip()
    # Python
    if ext == '.py':
        return line_strip.startswith('#'), False
    # C-like
    if 'multi' in syntax:
        start, end = syntax['multi']
        if in_multi_comment:
            if end in line_strip:
                return True, False
            return True, True
        if start in line_strip:
            if end in line_strip and line_strip.index(start) < line_strip.index(end):
                return True, False
            return True, True
    if 'single' in syntax and line_strip.startswith(syntax['single']):
        return True, False
    return False, False

def cloc_stat_in_dirs(dirs, exts):
    """
    类 cloc 统计：返回 {ext: {'files': n, 'blank': n, 'comment': n, 'code': n, 'lines': n}}
    """
    stats = {}
    for ext in exts:
        stats[ext] = {'files': 0, 'blank': 0, 'comment': 0, 'code': 0, 'lines': 0}
    for dir_path in dirs:
        for root, _, files in os.walk(dir_path):
            for file in files:
                for ext in exts:
                    if file.endswith(ext):
                        stats[ext]['files'] += 1
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                in_multi_comment = False
                                for line in f:
                                    stats[ext]['lines'] += 1
                                    if not line.strip():
                                        stats[ext]['blank'] += 1
                                    else:
                                        is_comment, in_multi_comment = detect_comment(line, ext, in_multi_comment)
                                        if is_comment:
                                            stats[ext]['comment'] += 1
                                        else:
                                            stats[ext]['code'] += 1
                        except Exception:
                            pass
    return stats
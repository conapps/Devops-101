#!/usr/bin/python
import os
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./server")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template('README.j2')

files = os.listdir('./diffs')
file_list = []

for f in files:
    if f.endswith('.md'):
        file_list.append(f)

template.stream(
    file_list=file_list
).dump('./diffs/README.md')

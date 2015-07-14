__author__ = 'bernhard'

import os
import shutil

from ext2rdf.src import main as e2rdf


def do_e2rdf(content, data_path=os.path.join('.', 'data')):

    temp_path = os.path.normpath(os.path.join(data_path, 'e2rdf_temp'))

    paths = {
        'input': os.path.join(temp_path, 'input'),
        'output': os.path.join(temp_path, 'output')
    }

    __clean_paths(temp_path)

    # write content to file
    with open(paths['input'], mode='w') as o:
        o.write(content)

    # run extractions and build nt
    e2rdf.convert_output_file(
        paths['input'],
        paths['output']
    )

    with open(paths['output'] + '.e2rdf', mode='r') as raw_extr:
        with open(paths['output'] + '.nt', mode='r') as nt_file:
            return raw_extr.read(), nt_file.read()


def __clean_paths(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path, mode=0o770)

__author__ = 'bernhard'

import os
import shutil

from qa_jbt.utils.paths import create_paths

from ext2rdf.src import main as e2rdf


def do_e2rdf(content, data_path=os.path.join('.', 'data')):

    temp_path = os.path.normpath(os.path.join(data_path, 'e2rdf_temp'))

    paths = {
        'input': os.path.join(temp_path, 'input'),
        'output': os.path.join(temp_path, 'output')
    }

    create_paths(data_path, temp_path)

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
            raw, nt = raw_extr.read(), nt_file.read()

    shutil.rmtree(temp_path)

    return raw, nt

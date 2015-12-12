#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np

    config = Configuration('_extensions', parent_package, top_path)

    sources = ["c/common", "c/convolution", "c/wavelets", "c/wt"]
    source_templates = ["c/convolution", "c/wt"]
    headers = ["c/templating", "c/wavelets_coeffs"]
    header_templates = ["c/convolution", "c/wt", "c/wavelets_coeffs"]

    c_files = ["{0}.c".format(s) for s in sources]
    depends = (["{0}.template.c".format(s) for s in source_templates]
               + ["{0}.template.h".format(s) for s in header_templates]
               + ["{0}.h".format(s) for s in headers]
               + ["{0}.h".format(s) for s in sources])

    config.add_extension('_pywt',
        sources=["_pywt.c"] + c_files,
        depends=["_dwt.c"] + depends,
        include_dirs=["c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension('_dwt',
        sources=["_dwt.c"] + c_files,
        depends=["_pywt.c"] + depends,
        include_dirs=["c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension('_swt',
        sources=["_swt.c"] + c_files,
        depends=["_pywt.c"] + depends,
        include_dirs=["c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from staticjinja import Renderer

# local
from bibpy import bib


def get_works():
    works = []
    for root, dirs, files in os.walk('bibtex'):
        # shuffle(files)
        for fn in filter(lambda fn: fn.endswith('bib'), files):
            parser = bib.Bibparser(bib.clear_comments(open(os.path.join(root, fn), 'r').read()))
            parser.parse()
            data = parser.records.values()[0]
            # teaser image url
            data['teaser'] = 'teaser_images/%s.jpg' % os.path.splitext(fn)[0]
            data['thumb'] = 'teaser_images/thumb/%s.jpg' % os.path.splitext(fn)[0]
            works.append(data)
    return {'works': works}


def main(argv=sys.argv[:]):
    template_folder = os.path.join(os.getcwd(), 'templates')
    renderer = Renderer(
            template_folder=template_folder,
            contexts=[
                ('index.html', get_works),
                ])
    renderer.run(debug=True, use_reloader=False)
    return 0

if __name__ == "__main__":
    sys.exit(main())

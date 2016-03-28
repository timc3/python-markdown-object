#!/usr/bin/env python

"""
Gets Object links in a Markdown document. 

Inspired by a simple YouTube mdx_youtube Markdown plugin

"""

import markdown
try:
    from markdown.util import etree
except:    
    from markdown import etree

version = "0.1.0"

class ObjectExtension(markdown.Extension):
    def __init__(self, configs):
        self.config = {
            'width': ['640', 'Width for Object embed'],
            'height': ['360', 'Height for Object embed'],
        }

        # Override defaults with user settings
        if configs:
            for key, value in configs.iteritems():
                self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        pattern = ObjectEmbed(r'([^(]|^)http[s]?:\/\/www\.youtube\.com\/watch\?\S*v=(?P<youtubeargs>[A-Za-z0-9_&=-]+)\S*')
        pattern.md = md
        pattern.ext = self
        md.inlinePatterns.add('object', pattern, "<reference")

class ObjectEmbed(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        url = 'https://www.youtube.com/v/%s' % m.group('youtubeargs')
        width = self.ext.config['width'][0]
        height = self.ext.config['height'][0]
        return object_object(url, width, height)

def object_object(url, width, height):
        obj = etree.Element('object')
        obj.set('width', width)
        obj.set('height', height)
        obj.set('data', url)
        return obj

def makeExtension(configs=None) :
    return ObjectExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

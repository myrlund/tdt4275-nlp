import os
from xml.dom import minidom
from xml.parsers import expat
from lxml import etree

def load_contents(corpus="brown1"):
    """
    Params:
        amount: 'all', 'first'.
        corpus: 'brown1', 'brown2', or 'brownv'
    """
    
    corpus_dir = "%s/tagfiles/" % corpus
    files = os.listdir(corpus_dir)
    f = open(corpus_dir + files[0])
    txt = f.read()
    f.close()
    return txt

def load_xml():
    txt = load_contents()
    parser = etree.XMLParser(recover=True)
    doc = etree.parse(txt, parser)
    # parser = expat.ParserCreate()
    # foo = parser.Parse(txt)
    # return foo
    print etree.tostring(doc)
    return doc

def load_traversed_text():
    d = os.path.dirname(__file__)
    fn = os.path.join(d, 'traversed/all2.txt')
    f = open(fn)
    txt = f.read()
    f.close()
    return txt

if __name__ == '__main__':
    print load_traversed_text()

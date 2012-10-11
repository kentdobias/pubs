import os
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
    
import files
import color
import pretty

class Paper(object):
    """Paper class. The object is responsible for the integrity of its own data,
    and for loading and writing it to disc.
    """

    @classmethod
    def from_disc(cls, name, citekey = None, number = None):
        bib_data = files.load_bibdata(self.name)
        metadata = files.load_meta(self.name)
        p = Paper(name, bib_data = bib_data, metadata = metadata, 
                        citekey = citekey, number = number)
        return p

    @classmethod
    def from_bibpdffiles(cls, pdfpath, bibpath):
        bib_data = cls.import_bibdata(bibpath)
        name, meta = cls.import_meta(pdfpath, bib_data)
        p = Paper(name, bib_data = bib_data, metadata = meta)
        
        return p            

    def __init__(self, name, bib_data = None, metadata = None, 
                       citekey = None, number = None):
        self.name = name
        self.bib_data = bib_data
        self.metadata = metadata
        self.citekey  = citekey
        self.number   = number
                
    def save_to_disc(self):
        files.write_bibdata(self.bib_data, self.name)
        files.write_meta(self.metadata, self.name)

    @classmethod
    def import_bibdata(cls, bibfile):        
        """Import bibligraphic data from a .bibyaml, .bib or .bibtex file"""
        fullbibpath = os.path.abspath(bibfile)
        files.check_file(fullbibpath)
        
        bib_data = files.load_externalbibfile(fullbibpath)
        print('{}bibliographic data present in {}{}{}'.format(
               color.grey, color.cyan, bibfile, color.end))
        print(pretty.bib_desc(bib_data))
        
        return bib_data

    @classmethod
    def import_meta(cls, pdfpath, bib_data):
    
        fullpdfpath = os.path.abspath(pdfpath)
        files.check_file(fullpdfpath)
    
        name, ext = files.name_from_path(pdfpath)
    
        meta = configparser.ConfigParser()
        meta.add_section('metadata')
    
        meta.set('metadata', 'name', name)
        meta.set('metadata', 'extension', ext)
        meta.set('metadata', 'path', os.path.normpath(fullpdfpath))
    
        meta.add_section('notes')
        
        return name, meta

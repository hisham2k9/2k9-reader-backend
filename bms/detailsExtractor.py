import os
import sys
import zipfile
from lxml import etree
from PIL import Image

def get_epub_cover(epub_path):
    ''' Return the cover image file from an epub archive. '''
    
    # We open the epub archive using zipfile.ZipFile():
    with zipfile.ZipFile(epub_path) as z:
    
        # We load "META-INF/container.xml" using lxml.etree.fromString():
        t = etree.fromstring(z.read("META-INF/container.xml"))
        # We use xpath() to find the attribute "full-path":
        '''
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" ... />
          </rootfiles>
        </container>
        '''
        rootfile_path =  t.xpath("/u:container/u:rootfiles/u:rootfile",
                                             namespaces=namespaces)[0].get("full-path")
        print("Path of root file found: " + rootfile_path)
        
        # We load the "root" file, indicated by the "full_path" attribute of "META-INF/container.xml", using lxml.etree.fromString():
        t = etree.fromstring(z.read(rootfile_path))
        # We use xpath() to find the attribute "content":
        '''
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
          ...
          <meta content="my-cover-image" name="cover"/>
          ...
        </metadata>
        '''
        cover_id = t.xpath("//opf:metadata/opf:meta[@name='cover']",
                                    namespaces=namespaces)[0].get("content")
        print("ID of cover image found: " + cover_id)
        
        # We use xpath() to find the attribute "href":
        '''
        <manifest>
            ...
            <item id="my-cover-image" href="images/978.jpg" ... />
            ... 
        </manifest>
        '''
        cover_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_id + "']",
                                         namespaces=namespaces)[0].get("href")
        # In order to get the full path for the cover image, we have to join rootfile_path and cover_href:
        cover_path = os.path.join(os.path.dirname(rootfile_path), cover_href)
        print("Path of cover image found: " + cover_path)
        
        # We return the image
        return z.open(cover_path)
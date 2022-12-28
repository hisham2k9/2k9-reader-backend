import os
import sys
import zipfile
from lxml import etree
from PIL import Image

namespaces = {
   "calibre":"http://calibre.kovidgoyal.net/2009/metadata",
   "dc":"http://purl.org/dc/elements/1.1/",
   "dcterms":"http://purl.org/dc/terms/",
   "opf":"http://www.idpf.org/2007/opf",
   "u":"urn:oasis:names:tc:opendocument:xmlns:container",
   "xsi":"http://www.w3.org/2001/XMLSchema-instance",
}
def get_epub_cover(epub_path):
    ''' Return the cover image file from an epub archive. '''
    
    # We open the epub archive using zipfile.ZipFile():
    try:
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
            cover_path = os.path.join(os.path.dirname(rootfile_path), cover_href).replace("\\","/")
            #cover_path = rootfile_path
            print("Path of cover image found: " + cover_path)
            print(type(cover_path))
            # We return the image
            with z.open(cover_path) as file: # b is important -> binary
                fileContent = file.read()
            return fileContent
    except:
        return None



def epub_info(fname):
    try:
        def xpath(element, path):
            return element.xpath(
                path,
                namespaces={
                    "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                    "pkg": "http://www.idpf.org/2007/opf",
                    "dc": "http://purl.org/dc/elements/1.1/",
                },
            )[0]

        # prepare to read from the .epub file
        zip_content = zipfile.ZipFile(fname)
        
        # find the contents metafile
        cfname = xpath(
            etree.fromstring(zip_content.read("META-INF/container.xml")),
            "n:rootfiles/n:rootfile/@full-path",
        ) 
        
        # grab the metadata block from the contents metafile
        metadata = xpath(
            etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata"
        )
        
        # repackage the data
        return {
            s: xpath(metadata, f"dc:{s}/text()")
            for s in ("title", "language", "creator", "date", "identifier")
        }   
    except:
        return {"title":"","language":"","creator":"","date":"","identifier":""}
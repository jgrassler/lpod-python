# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from the Standard Library
from copy import deepcopy
from datetime import datetime

# Import from lpod
from container import ODF_PARTS, odf_get_container
from container import odf_new_container_from_type, odf_container
from container import odf_new_container_from_template
from content import odf_content
from meta import odf_meta
from styles import odf_styles
from utils import Date, DateTime, _set_value_and_type
from utils import Duration
from xmlpart import odf_create_element, odf_element
from xmlpart import odf_xmlpart, LAST_CHILD


#
# odf creation functions
#

def odf_create_section(style=None):
    """Create a section element of the given style.

    Arguments:

        style -- str

    Return: odf_element
    """
    element = odf_create_element('<text:section/>')
    if style:
        element.set_attribute('text:style-name', style)
    return element



def odf_create_paragraph(text=None, style=None):
    """Create a paragraph element of the given style containing the optional
    given text.

    Arguments:

        style -- str

        text -- unicode

    Return: odf_element
    """
    element = odf_create_element('<text:p/>')
    if text:
        element.set_text(text)
    if style:
        element.set_attribute('text:style-name', style)
    return element



def odf_create_span(text=None, style=None):
    """Create a span element of the given style containing the optional
    given text.

    Arguments:

        style -- str

        text -- unicode

    Return: odf_element
    """
    element = odf_create_element('<text:span/>')
    if text:
        element.set_text(text)
    if style:
        element.set_attribute('text:style-name', style)
    return element



def odf_create_heading(level, text=None, style=None):
    """Create a heading element of the given style and level, containing the
    optional given text.

    Level count begins at 1.

    Arguments:

        level -- int

        style -- str

        text -- unicode

    Return: odf_element
    """
    data = '<text:h text:outline-level="%d"/>'
    element = odf_create_element(data % level)
    if text:
        element.set_text(text)
    if style:
        element.set_attribute('text:style-name', style)
    return element



def odf_create_frame(name, width, height, page=None, x=None, y=None, style=None):
    """Create a frame element of the given style, width and height,
    optionally positionned at the given x and y coordinates in the given
    page number.

    Width, height, x and y are strings including the units, e.g. "10cm".

    Arguments:

        width -- str

        height -- str

        page -- int

        x -- str

        y -- str

        style -- str

    Return: odf_element
    """
    if page is None:
        options = 'text:anchor-type="paragraph"'
    else:
        options = 'text:anchor-type="page" text:anchor-page-number="%d"' % page
        if x is not None:
            options += ' svg:x="%s"' % x
        if y is not None:
            options += ' svg:y="%s"' % y
    data = '<draw:frame draw:name="%s" svg:width="%s" svg:height="%s" %s/>'
    element = odf_create_element(data % (name, width, height, options))
    if style:
        element.set_attribute('draw:style-name', style)
    return element



def odf_create_image(uri):
    """Create an image element showing the image at the given URI.

    Arguments:

        uri -- str

    Return: odf_element
    """
    return odf_create_element('<draw:image xlink:href="%s"/>' % uri)



def odf_create_cell(value=None, representation=None, cell_type=None,
                    currency=None):
    """Create a cell element containing the given value. The textual
    representation is automatically formatted but can be provided. Cell type
    can be deduced as well, unless the number is a percentage or currency. If
    cell type is "currency", the currency must be given.

    Arguments:

        value -- bool, int, float, Decimal, date, datetime, str, unicode,
                 timedelta

        representation -- unicode

        cell_type -- 'boolean', 'currency', 'date', 'float', 'percentage',
                     'string' or 'time'

        currency -- three-letter str

    Return: odf_element
    """

    cell = odf_create_element('<table:table-cell/>')
    representation = _set_value_and_type(cell, value=value,
                                         representation=representation,
                                         value_type=cell_type,
                                         currency=currency)
    if representation is not None:
        cell.set_text_content(representation)
    return cell



def odf_create_row(width=None):
    """Create a row element, optionally filled with "width" number of cells.

    Arguments:

        width -- int

    Return: odf_element
    """
    row = odf_create_element('<table:table-row/>')
    if width is not None:
        for i in xrange(width):
            cell = odf_create_cell(u"")
            row.insert_element(cell, LAST_CHILD)
    return row



def odf_create_column(style=None):
    """Create a column element of the optionally given style.

    Arguments:

        style -- str

    Return: odf_element
    """
    element = odf_create_element('<table:table-column/>')
    if style:
        element.set_attribute('table:style-name', style)
    return element



def odf_create_table(name, width=None, height=None, style=None):
    """Create a table element, optionally prefilled with "width" columns and
    "height" rows, and of the optionally given style.

    Arguments:

        width -- int

        height -- int

        style -- str

    Return: odf_element
    """
    name = name.encode('utf_8')
    element = odf_create_element('<table:table table:name="%s"/>' % name)
    if width is not None or height is not None:
        width = width if width is not None else 1
        height = height if height is not None else 1
        for i in xrange(height):
            row = odf_create_row(width)
            element.insert_element(row, LAST_CHILD)
    if style:
        element.set_attribute('table:style-name', style)
    return element



def odf_create_list_item(text=None):
    """Create a list item element.

    The "text" argument is just a shortcut for the most common case. To
    create a list item with several paragraphs or anything else (except
    tables), first create an empty list item, and fill it using the other
    "odf_create_*" functions.

    Arguments:

        text -- unicode

    Return: odf_element
    """
    element = odf_create_element('<text:list-item/>')
    if text is not None:
        element.set_text_content(text)
    return element



def odf_create_list(text=[], style=None):
    """Create a list element.

    Arguments:

        text -- a list of unicode

        style -- str

    The "text" argument is just a shortcut for the most common case. To create
    complex lists, first create an empty list, and fill it using built list
    items.

    Return: odf_element
    """
    element = odf_create_element('<text:list/>')
    for value in text:
        element.append_element(odf_create_list_item(text=value))
    if style is not None:
        element.set_attribute('text:style-name', style)
    return element



def odf_create_style(name, family, area=None, **kw):
    """Create a style element with the given name, related to the given
    family.

    Arguments:

        name -- str

        family -- 'paragraph', 'text', 'section', 'table', 'tablecolumn',
                  'table-row', 'table-cell', 'table-page', 'chart',
                  'default', 'drawing-page', 'graphic', 'presentation',
                  'control' or 'ruby'

        area -- the "<area>-properties" where to store properties,
                identical to the family by default

        kw -- properties to create on the fly

    Return: odf_element
    """
    data = '<style:style style:name="%s" style:family="%s"/>'
    element = odf_create_element(data % (name, family))
    if kw:
        if area is None:
            area = family
        element.set_style_properties(kw, area=area)
    return element



def odf_create_note(text, note_class='footnote', id=None, body=None):
    """Create either a footnote or a endnote element with the given text,
    optionally referencing it using the given id.

    Arguments:

        text -- unicode

        note_class -- 'footnote' or 'endnote'

        id -- str

        body -- an odf_element or an unicode object

    Return: odf_element
    """
    data = ('<text:note text:note-class="%s">'
              '<text:note-citation>%s</text:note-citation>'
              '<text:note-body/>'
            '</text:note>')
    text = text.encode('utf_8')
    element = odf_create_element(data % (note_class, text))
    if id is not None:
        element.set_attribute('text:id', id)
    if body is not None:
        note_body = element.get_element('text:note-body')
        # Autocreate a paragraph if body = unicode
        if isinstance(body, unicode):
            note_body.set_text_content(body)
        elif isinstance(body, odf_element):
            note_body.insert_element(body, LAST_CHILD)
        else:
            raise ValueError, 'unexpected type for body: "%s"' % type(body)
    return element



def odf_create_annotation(creator, text, date=None):
    """Create an annotation element credited to the given creator with the
    given text, optionally dated (current date by default).

    Arguments:

        creator -- unicode

        text -- unicode

        date -- datetime

    Return: odf_element
    """
    # TODO allow paragraph and text styles
    data = ('<office:annotation>'
               '<dc:creator>%s</dc:creator>'
               '<dc:date>%s</dc:date>'
               '<text:p>%s</text:p>'
            '</office:annotation>')
    creator = creator.encode('utf_8')
    if date is None:
        date = datetime.now()
    date = DateTime.encode(date)
    text = text.encode('utf_8')
    return odf_create_element(data % (creator, date, text))



def odf_create_variable_decls():
    return odf_create_element('<text:variable-decls />')



def odf_create_variable_decl(name, value_type):
    data = '<text:variable-decl office:value-type="%s" text:name="%s"/>'
    return odf_create_element(data % (value_type, name))



def odf_create_variable_set(name, value, value_type=None, display=False,
                            representation=None, style=None):
    data = '<text:variable-set text:name="%s" />'
    element = odf_create_element(data % name)
    representation = _set_value_and_type(element, value=value,
                                         value_type=value_type,
                                         representation=representation)
    if not display:
        element.set_attribute('text:display', 'none')
    else:
        element.set_text(representation)
    if style is not None:
        element.set_attribute('style:data-style-name', style)
    return element



def odf_create_variable_get(name, value, value_type=None,
                            representation=None, style=None):
    data = '<text:variable-get text:name="%s" />'
    element = odf_create_element(data % name)
    representation = _set_value_and_type(element, value=value,
                                         value_type=value_type,
                                         representation=representation)
    element.set_text(representation)
    if style is not None:
        element.set_attribute('style:data-style-name', style)
    return element



def odf_create_user_field_decls():
    return odf_create_element('<text:user-field-decls />')



def odf_create_user_field_decl(name, value, value_type=None):
    data = '<text:user-field-decl text:name="%s"/>'
    element = odf_create_element(data % name)
    _set_value_and_type(element, value=value, value_type=value_type)
    return element



def odf_create_user_field_get(name, value, value_type=None,
                              representation=None, style=None):
    data = '<text:user-field-get text:name="%s" />'
    element = odf_create_element(data % name)
    representation = _set_value_and_type(element, value=value,
                                         value_type=value_type,
                                         representation=representation)
    element.set_text(representation)
    if style is not None:
        element.set_attribute('style:data-style-name', style)
    return element



def odf_create_page_number_variable(select_page=None, page_adjust=None):
    """page_adjust is an integer to add (or subtract) to the page number

    select_page -- string in ('previous', 'current', 'next')
    page_adjust -- int
    """
    element = odf_create_element('<text:page-number/>')
    if select_page is None:
        select_page = 'current'
    element.set_attribute('text:select-page', select_page)
    if page_adjust is not None:
        element.set_attribute('text:page-adjust', str(page_adjust))
    return element



def odf_create_page_count_variable():
    return odf_create_element('<text:page-count />')



def odf_create_date_variable(date, fixed=False, data_style=None,
                             representation=None, date_adjust=None):
    data = '<text:date text:date-value="%s"/>'
    element = odf_create_element(data % DateTime.encode(date))
    if fixed:
        element.set_attribute('text:fixed', 'true')
    if data_style is not None:
        element.set_attribute('style:data-style-name', data_style)
    if representation is None:
        representation = Date.encode(date)
    element.set_text(representation)
    if date_adjust is not None:
        element.set_attribute('text:date-adjust',
                               Duration.encode(date_adjust))
    return element



def odf_create_time_variable(time, fixed=False, data_style=None,
                             representation=None, time_adjust=None):
    data = '<text:time text:time-value="%s"/>'
    element = odf_create_element(data % DateTime.encode(time))
    if fixed:
        element.set_attribute('text:fixed', 'true')
    if data_style is not None:
        element.set_attribute('style:data-style-name', data_style)
    if representation is None:
        representation = time.strftime('%H:%M:%S')
    element.set_text(representation)
    if time_adjust is not None:
        element.set_attribute('text:time-adjust',
                               Duration.encode(time_adjust))
    return element



def odf_create_chapter_variable(display='name', outline_level=None):
    """display can be: 'number', 'name', 'number-and-name', 'plain-number' or
                       'plain-number-and-name'
    """
    data = '<text:chapter text:display="%s"/>'
    element = odf_create_element(data % display)
    if outline_level is not None:
        element.set_attribute('text:outline-level', str(outline_level))
    return element



def odf_create_filename_variable(display='full', fixed=False):
    """display can be: 'full', 'path', 'name' or 'name-and-extension'
    """
    data = '<text:file-name text:display="%s"/>'
    element = odf_create_element(data % display)
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_initial_creator_variable(fixed=False):
    element = odf_create_element('<text:initial-creator/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_creation_date_variable(fixed=False, data_style=None):
    element = odf_create_element('<text:creation-date/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    if data_style is not None:
        element.set_attribute('style:data-style-name', data_style)
    return element



def odf_create_creation_time_variable(fixed=False, data_style=None):
    element = odf_create_element('<text:creation-time/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    if data_style is not None:
        element.set_attribute('style:data-style-name', data_style)
    return element



def odf_create_description_variable(fixed=False):
    element = odf_create_element('<text:description/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_title_variable(fixed=False):
    element = odf_create_element('<text:title/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_subject_variable(fixed=False):
    element = odf_create_element('<text:subject/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_keywords_variable(fixed=False):
    element = odf_create_element('<text:keywords/>')
    if fixed:
        element.set_attribute('text:fixed', 'true')
    return element



def odf_create_draw_page(name, style=None, master_page=None,
                         page_layout=None, id=None):
    """This element is a container for content in a drawing or presentation
    document.

    Arguments:

        name -- unicode

        style -- str

        master_page -- str

        page_layout -- str

        id -- str

    Return: odf_element
    """
    element = odf_create_element('<draw:page/>')
    element.set_attribute('draw:name', name.encode('utf_8'))
    if style:
        element.set_attribute('draw:style-name', style)
    if master_page:
        element.set_attribute('draw:master-page-name', master_page)
    if page_layout:
        element.set_attribute('presentation:presentation-page-layout-name',
                              page_layout)
    if id:
        element.set_attribute('draw:id', id)
    return element



#
# The odf_document object
#

class odf_document(object):
    """Abstraction of the ODF document.
    """
    def __init__(self, container):
        if not isinstance(container, odf_container):
            raise TypeError, "container is not an ODF container"
        self.container = container

        # Cache of XML parts
        self.__xmlparts = {}

        # Cache of the body
        self.__body = None


    #
    # Public API
    #

    def get_xmlpart(self, part_name):
        if part_name not in ODF_PARTS:
            raise ValueError, '"%s" is not an XML part' % part_name
        parts = self.__xmlparts
        part = parts.get(part_name)
        if part is None:
            container = self.container
            if part_name == 'content':
                part = odf_content(part_name, container)
            elif part_name == 'meta':
                part = odf_meta(part_name, container)
            elif part_name == 'styles':
                part = odf_styles(part_name, container)
            else:
                part = odf_xmlpart(part_name, container)
            parts[part_name] = part
        return part


    def get_type(self):
        """
        Get the ODF type (also called class) of this document.

        Return: 'chart', 'database', 'formula', 'graphics',
            'graphics-template', 'image', 'presentation',
            'presentation-templatemplate', 'spreadsheet',
            'spreadsheet-template', 'text', 'text-master',
            'text-template' or 'text-web'
        """

        mimetype = self.container.get_part('mimetype').strip()

        # The mimetype must be with the form:
        # application/vnd.oasis.opendocument.text

        # Isolate and return the last part
        return mimetype.split('.')[-1]


    def get_body(self):
        if self.__body is None:
            content = self.get_xmlpart('content')
            type = self.get_type()
            if type == 'text':
                self.__body = content.get_text_body()
            elif type == 'spreadsheet':
                self.__body = content.get_spreadsheet_body()
            elif type == 'presentation':
                self.__body = content.get_presentation_body()
            else:
                raise NotImplementedError
        return self.__body


    def clone(self):
        """Return an exact copy of the document.
        Return: odf_document
        """
        clone = object.__new__(self.__class__)
        for name in self.__dict__:
            if name == 'container':
                setattr(clone, name, self.container.clone())
            elif name == '_odf_document__xmlparts':
                xmlparts = {}
                for key, value in self.__xmlparts.iteritems():
                    xmlparts[key] = value.clone()
                setattr(clone, name, xmlparts)
            else:
                value = getattr(self, name)
                value = deepcopy(value)
                setattr(clone, name, value)
        return clone


    def save(self, uri=None, packaging=None, pretty=False):
        """Save the document, at the same place it was opened or at the given
        URI. It can be saved as a Zip file or as a plain XML file. The XML
        can be pretty printed.
        Arguments:

            uri -- str
            packaging -- 'zip' or 'flat'
            pretty -- bool
        """
        # Synchronize data with container
        for part_name, part in self.__xmlparts.items():
            if part is not None:
                self.container.set_part(part_name, part.serialize(pretty))

        # Save the container
        self.container.save(uri, packaging)


    #
    # Styles over several parts
    #

    def get_style_list(self, family=None, category=None):
        attributes = {}
        if family is not None:
            attributes['style:family'] = family
        styles = self.get_xmlpart('styles')
        if category is None or category == 'automatic':
            content = self.get_xmlpart('content')
            return (styles.get_style_list(family=family, category=category)
                    + content.get_style_list(family=family,
                                             category=category))
        return styles.get_style_list(family=family, category=category)


    def get_style(self, name, family, retrieve_by='name'):
        # 1. content
        # TODO except retrieve_by is "display-name"
        content = self.get_xmlpart('content')
        element = content.get_style(name, family)
        if element is not None:
            return element
        # 2. styles
        styles = self.get_xmlpart('styles')
        return styles.get_style(name, family, retrieve_by=retrieve_by)



#
# odf_document factories
#

def odf_get_document(uri):
    """Return an "odf_document" instance of the ODF document stored at the
    given URI.

    Example::

        >>> uri = 'uri://of/a/document.odt'
        >>> document = odf_get_document(uri)
    """
    container = odf_get_container(uri)
    return odf_document(container)



def odf_new_document_from_template(template_uri):
    """Return an "odf_document" instance using the given template.

    Example::

        >>> uri = 'uri://of/a/template.ott'
        >>> document = odf_new_document_from_template(uri)
    """
    container = odf_new_container_from_template(template_uri)
    return odf_document(container)



def odf_new_document_from_type(odf_type):
    """Return an "odf_document" instance of the given type.
    Arguments:

        odf_type -- 'text', 'spreadsheet', 'presentation' or 'drawing'

    Example::

        >>> document = odf_new_document_from_type('spreadsheet')
    """
    container = odf_new_container_from_type(odf_type)
    return odf_document(container)


"""
"""

import os
from pprint import pprint
import tempfile
from urllib import pathname2url
import webbrowser

import view
import serialise


class IoFacade(object):

    _load_delegate = {
        # "csv":   _load_csv,
        "json":  serialise.load_json,
        "xml":   serialise.load_xml,
    }

    _write_delegate = {
        # "csv":   _write_csv,
        "json":  serialise.write_json,
        "xml":   serialise.write_xml,
    }

    @staticmethod
    def load_from_file(filepath, format_=None):
        """Load abstract-formatted data from a stream.

        Returns:
            dict.
        """
        format_ = format_ if format_ else os.path.splitext(filepath)[-1][1:]

        load_func = IoFacade._load_delegate[format_]
        print "Ingesting '{ext}' as: '{bn}'".format(
            bn=filepath, ext=format_.upper())
        with open(filepath, 'r') as ff:
            data = load_func(ff, filepath=filepath)

        return data

    @staticmethod
    def write_to_file(data, filepath, format_=None):
        """Write abstract-formatted data.

        Returns:
            True - If writen file is found.
        """
        format_ = format_ if format_ else os.path.splitext(filepath)[-1][1:]

        write_func = IoFacade._write_delegate[format_]
        success = write_func(data, filepath)
        if success:
            print "Saved '{ext}' successfully as: '{bn}'".format(
                bn=filepath, ext=format_.upper())
        else:
            print "Failed to export data to {}".format(filepath)
            return False
        return success

    @staticmethod
    def supported():
        """Return supported storage formats.
        """
        return [attr for attr in IoFacade._load_delegate.keys()]


###############################################################################
class RenderFacade(object):

    _delegate = {
        'console': {'writer': view.TextWriter, 'func': 'render_console'},
        'html':    {'writer': view.HtmlWriter, 'func': 'render_html'},
    }

    def __init__(self, data, infilepath, render_choice):
        self._data = data
        self._infilepath = infilepath
        title = "\nSource data path: '{}'".format(self._infilepath)
        self._render_choice = render_choice
        self._writer = self._delegate[render_choice]['writer']
        self._render_maker = view.RenderMaker(title, self._writer())

    # TODO: order fields
    def render_console(self):
        """Render data to console stdout.
        """
        for key, fields in self._sorted_data():
            self._render_maker.add_paragraph(
                '{sep}\nid: {k}'.format(sep=self._sep(), k=key)
                )
            fields_text = ['   {n}: {t}'.format(n=name, t=text)
                           for name, text in fields.iteritems()
                           ]
            self._render_maker.add_paragraph('\n'.join(fields_text))

        print self._render_maker.render()

    def render_html(self):
        """Render data to a temp html file and read in webbrowser.
        """
        for key, fields in self._sorted_data():
            self._render_maker.add_paragraph('{sep}<br />id: {k}'.format(
                sep=self._sep, k=key)
                )
            fields_text = ['   {n}: {t}'.format(n=name, t=text)
                           for name, text in fields.iteritems()]
            self._render_maker.add_paragraph('<br />'.join(fields_text))
        self._render_maker.render()
        self._open_html()

        return self._render_maker.output.getvalue()

    def _open_html(self):
        tmp = tempfile.TemporaryFile(suffix=".html", delete=False)
        tmp.write(self.output_value)
        url = 'file:{}'.format(pathname2url(os.path.abspath(tmp.name)))
        webbrowser.open(url)

    def do_render(self):
        render_func = getattr(self, self._delegate[self._render_choice]['func'])
        return render_func()

    def _sorted_data(self):
        return sorted(self._data.items(), key=lambda x: x[0])

    @property
    def output_value(self):
        return self._render_maker.output_value

    @staticmethod
    def _sep():
        return "#" * 80

    @staticmethod
    def supported():
        """Return supported render formats.
        """
        return [attr for attr in RenderFacade._delegate.keys()]


###############################################################################
class Manager(object):

    def __init__(self, infile, outfile=None):
        if not os.path.isfile(infile):
            raise IOError("Can't find: {}".format(infile))
        self._infile = infile
        self._outfile = outfile
        self._data = None

    def load_file(self, **kwarg):
        """Ingest data from infile.
        """
        self._data = IoFacade.load_from_file(self._infile, kwarg)
        return self._data

    def convert_source_file(self):
        """Convert ingested data into the outfile's format.
        """
        if not self._data:
            raise ValueError("self._data val is empty!")
        return IoFacade.write_to_file(self._data, self._outfile)

    def render_data(self, renderer='console'):
        """Render data derived from the renderer paramater.
        """
        if not self._data:
            raise ValueError("self._data val is empty!")

        render_facade = RenderFacade(self._data, self._infile, renderer)
        render_facade.do_render()
        self._output_value = render_facade.output_value

    @property
    def infile(self):
        return self._infile

    @property
    def outfile(self):
        return self._outfile

    @property
    def output_value(self):
        return self._output_value

    @property
    def data(self):
        return self._data

    @staticmethod
    def supported_formats():
        return IoFacade.supported()

    @staticmethod
    def supported_renderers():
        return RenderFacade.supported()

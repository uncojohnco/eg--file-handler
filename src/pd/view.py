"""
View module for rendering data to screen.
"""

import os
import sys
from xml.sax.saxutils import escape
import textwrap
import StringIO


### Writers ###################################################################
class BaseWriter(object):

    def __init__(self, output):
        self._output = output

    def header(self):
        raise NotImplementedError("Not Yet Implemented!")

    def title(self, title):
        raise NotImplementedError("Not Yet Implemented!")

    def start_body(self):
        raise NotImplementedError("Not Yet Implemented!")

    def body(self, text):
        raise NotImplementedError("Not Yet Implemented!")

    def end_body(self):
        raise NotImplementedError("Not Yet Implemented!")

    def footer(self):
        raise NotImplementedError("Not Yet Implemented!")

    @property
    def output(self):
        return self._output

    @property
    def output_value(self):
        return self._output.getvalue()


class TextWriter(BaseWriter):

    def __init__(self, width=80, output=StringIO.StringIO()):
        super(TextWriter, self).__init__(output)
        self.width = width

    def header(self):
        pass

    def title(self, title):
        lines = []
        lines.append("{t:^{w}}".format(
                 t=' %s ' % title, w=self.width).rstrip())
        lines.append("{ul:^{w}}".format(
                 ul=("=" * len(title)), w=self.width).rstrip())
        self._output.write('\n'.join(lines))


    def start_body(self):
        self._output.write("\n")

    def body(self, text):
        self._output.write(text)
        self._output.write("\n")

    def end_body(self):
        self._output.write("\n")

    def footer(self):
        pass


class HtmlWriter(BaseWriter):

    def __init__(self, output=StringIO.StringIO()):
        super(HtmlWriter, self).__init__(output)

    def header(self):
        self._output.write("<!doctype html>\n<html>\n")

    def title(self, title):
        self._output.write("<head><title>{}</title></head>\n".format(
            escape(title)))

    def start_body(self):
        self._output.write("<body>\n")

    def body(self, text):
        self._output.write("<p>{}</p>\n".format(text))

    def end_body(self):
        self._output.write("</body>\n")

    def footer(self):
        self._output.write("</html>\n")


###############################################################################
class RenderMaker(object):

    def __init__(self, title, writer):
        if not isinstance(writer, BaseWriter):
            "{} is not inherited from BaseWriter".format(writer)
        self._title = title
        self._writer = writer
        self._entries = []

    def add_paragraph(self, text):
        self._entries.append(text)

    def _pre_render(self):
        # header
        self._writer.header()
        self._writer.title(self._title)
        self._writer.start_body()

        # body
        for text in self._entries:
            self._writer.body(text)

        # footer
        self._writer.end_body()
        self._writer.footer()

        return self._writer.output_value

    def render(self):
        return self._pre_render()
        # TODO:
        # raise NotImplementedError("Not Yet Implemented!")

    @property
    def paragraphs(self):
        return self._entries

    @property
    def output(self):
        return self._writer.output

    @property
    def output_value(self):
        return self._writer.output_value

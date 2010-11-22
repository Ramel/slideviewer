# -*- coding: UTF-8 -*-
# Copyright (C) 2009-2010 Henry OBEIN <henry@itaapy.com>
# Copyright (C) 2010 Armel FORTUN <armel@tchack.com>
# Copyright (C) 2010 Hervé CAUWELIER <herve@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from itools
from itools.gettext import MSG
from itools.datatypes import Integer, Unicode, Boolean, String
from itools.core import merge_dicts, get_abspath
from itools.web import get_context
from itools.handlers import ro_database, File as FileHandler

# Import from ikaaro
from ikaaro.registry import register_resource_class
from ikaaro.table import OrderedTableFile
from ikaaro.menu import Target
from ikaaro.file import Image
from ikaaro.resource_ import DBResource

# Import from itws
from itws.bar import register_box
from itws.bar.diaporama import Diaporama, DiaporamaTable
from itws.datatypes import ImagePathDataType

from slideviewer_views import Slideviewer_View, SlideviewerTable_CompositeView


class SlideviewerTableFile(OrderedTableFile):

    record_properties = {
        'title': Unicode(multiple=True),
        'description': Unicode(multiple=True),
        'img_path': ImagePathDataType(multiple=True,
            mandatory=True), # multilingual
        'img_link': String,
        'target': Target(mandatory=True, default='_top')}


class SlideviewerTable(DiaporamaTable):

    class_id = 'slideviewer-table'
    class_handler = SlideviewerTableFile

    view = SlideviewerTable_CompositeView()


class Slideviewer(Diaporama):

    class_id = 'slideviewer'
    class_version = '20101022'
    class_title = MSG(u'Slideviewer')
    class_description = MSG(u'Slideviewer')

    # Configuration
    use_fancybox = False
    allow_instanciation = True
    is_content = True
    is_side = True

    # order
    order_class = SlideviewerTable

    edit_schema = {
        'width': Integer(default=256),
        'height': Integer(default=256),
        'border': Unicode(default="#FF0000"),
        'show_border': Boolean(default=True),
        'show_title': Boolean(default=True)
        }

    class_schema = merge_dicts(Diaporama.class_schema,
                                edit_schema)

    def init_resource(self, **kw):
        Diaporama.init_resource(self, **kw)
        # Check if the loading image is here!
        context = get_context()
        # XXX from handler level to the resource one,
        # finding the site_root and indexing image
        site_root = context.site_root
        if site_root.get_resource('images/loading', soft=True) is None:
            path = get_abspath('ui/loading.gif')
            with open(path) as file:
                body = file.read()
            site_root.make_resource('images/loading', Image,
                    format='image/gif', filename='loading.gif',
                    extension='gif', state='public', body=body)

    ##############
    # Views
    ##############
    view = Slideviewer_View()

    def update_20101022(self):
        if self.has_property('square'):
            print("Delete 'square' property")
            self.del_property('square')
            print("Delete 'square' property to %s" % self.get_property('title'))

    def update_20101021(self):
        if not self.has_property('show_border'):
            print("Add 'show_border' property to %s" % self.get_property('title'))
            self.set_property('show_border', False)
            print("'show_border' = %s" % self.get_property('show_border'))

    def update_20101020(self):
        if self.has_property('show_title'):
            print("'show_title' = %s" % self.get_property('show_title'))
        else:
            print("Add 'show_title' property to %s" % self.get_property('title'))
            self.set_property('show_title', False)
            print("'show_title' = %s" % self.get_property('show_title'))


class SlideviewerPro(Slideviewer):

    class_id = 'slideviewer-pro'
    class_version = '20101110'
    class_title = MSG(u'Slideviewer Pro')
    class_description = MSG(u'Slideviewer Pro')

    view = Slideviewer_View()

    @staticmethod
    def _make_resource(cls, folder, name, **kw):
        Slideviewer._make_resource(cls, folder, name, **kw)

    @classmethod
    def get_metadata_schema(cls):
        return merge_dicts(Diaporama.get_metadata_schema(),
            {'width': Integer(default=256),
            'height': Integer(default=256),
            'border': Unicode(default="#FF0000"),
            'show_border': Boolean(default=True),
            'show_title': Boolean(default=True),
            ## slideViewerPro options (defaults)
            # The border width around the main images 
            'galBorderWidth': Integer(default=6),
            # The distance that separates the thumbnails
            # and the buttons from the main images 
            'thumbsTopMargin': Integer(default=3),
            # The distance of each thumnail respect to the next one 
            'thumbsRightMargin': Integer(default=3),            
            # The border width of each thumbnail.
            # Note that the border in reality is above, not around 
            'thumbsBorderWidth': Integer(default=3),            
            # The width of the prev/next buttons that commands the thumbnails 
            'buttonsWidth': Integer(default=20),            
            # The border color around the main
            'galBorderColor': Unicode(default="#ff0000"),
            # The border color of the thumbnails but not the current one 
            'images thumbsBorderColor': Unicode(default="#d8d8d8"),
            # The border color of the current thumbnail 
            'thumbsActiveBorderColor': Unicode(default="#ff0000"),
            # The color of the optional text in leftButtonInner/rightButtonInner 
            'buttonsTextColor': Unicode(default="#ff0000"),
            # Could be 0, 0.1 up to 1.0
            'thumbsBorderOpacity': Decimal(default=1.0),
            # Could be 0, 0.1 up to 1.0 
            'thumbsActiveBorderOpacity': Decimal(default=1.0),
            # The time it takes a slide to move to its position 
            'easeTime': Integer(default=750),
            # If autoslide is true, this is the interval between each slide 
            'asTimer': Integer(default=4000),            
            # The number of visible thumbnails
            'thumbs': Integer(default=5),     
            # The percentual reduction of the thumbnails in relation to the original 
            'thumbsPercentReduction': Integer(default=12),
            # With this option set to false,
            # the whole UI (thumbs and buttons) are not visible
            'thumbsVis': Boolean(default=True),            
            # Could be an image "<img src='images/larw.gif' />" or an escaped
            # char as "&larr;" 
            'leftButtonInner': Unicode(default="-"),             
            # could be an image or an escaped char as "&rarr;"
            'rightButtonInner': Unicode(default="+"),            
            # By default the slider do not slides automatically.
            # When set to true REQUIRES the jquery.timers plugin 
            'autoslide': Boolean(default=False),
            # The typographic info of each slide.
            # When set to true, the ALT tag content is displayed 
            'typo': Boolean(default=False),             
            # The opacity for typographic info. 1 means fully visible. 
            'typoFullOpacity': Decimal(default=0.9),
            # The LI items can be shuffled (randomly mixed) when shuffle is true 
            'shuffle': Boolean(default=False)
            })


################################################################################
# Register
################################################################################
register_resource_class(Slideviewer)
#register_resource_class(SlideviewerPro)
register_box(Slideviewer)
#register_box(SlideviewerPro)

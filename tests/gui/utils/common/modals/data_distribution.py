"""Utils and fixtures to facilitate operations on Data distribution modal.
"""

__author__ = "Bartosz Walkowicz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebElement, WebItemsSequence,
                                               WebItem, Label, Button)
from .modal import Modal


class _Chunk(PageObject):
    start = Label('.chunks-scale.lower-size')
    end = Label('.chunks-scale.upper-size')
    _canvas = WebElement('canvas')
    _file_chunks = WebElement('.chunks-container')
    _file_chunks_text = WebElement('.chunks-container .chunks-text')

    def __str__(self):
        return 'file blocks for {}'.format(self.parent)

    @property
    def size(self):
        end, unit = self.end.split()
        start, _ = self.start.split()
        return int(end) - int(start), unit

    def chunks(self, file_size):
        chunks = self.driver.execute_script(_canvas_fill, self._canvas)
        if chunks is not False:
            return [(chunk[0]*file_size, chunk[1]*file_size)
                    for chunk in chunks]
        else:
            raise RuntimeError('{} is not filled correctly: some columns '
                               'are not filled with one color'.format(self))

    def is_never_synchronized(self):
        return 'never-synchronized-text' in self._file_chunks_text.get_attribute('class')


class _DataDistributionRecord(PageObject):
    name = id = Label('.oneprovider-name', parent_name='given provider')
    distribution = WebItem('.chunks-container', cls=_Chunk)
    menu_button = Button('.collapsible-toolbar-toggle')
    never_synchronized_text = WebElement('.never-synchronized-text')
    #  TODO: change test because of a new gui
    # migrate = Button('.btn-migrate')
    # replicate = Button('.btn-replicate')

    def __str__(self):
        return 'provider record for "{item}" in ' \
               '{parent}'.format(item=self.name, parent=self.parent)


class MigrationRecord(PageObject):
    name = id = Label('.item-label')

    def select(self):
        self.web_elem.click()

    def __str__(self):
        return 'provider record in migration menu in {}'.format(self.parent)


class DataDistributionModal(Modal):
    file_name = Label('.file-name')
    providers = WebItemsSequence('.oneproviders-distribution-item',
                                 cls=_DataDistributionRecord)
    #  TODO: change test because of a new gui
    # migrate = WebItemsSequence('.migrate-popover li.migrate-item',
    #                            cls=MigrationRecord)

    def __str__(self):
        return 'Data distribution modal for "{}"'.format(self.file_name)

    def size(self):
        provider_record = self.providers[0].distribution
        end, unit = provider_record.end.split()
        start, _ = provider_record.start.split()
        return int(end) - int(start)


# TODO fix not working commented code
# In case when fill color of canvas is changed,
# variable fillColor must also change to new value
_canvas_fill = """
function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length != b.length) return false;

    for (var i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}


function isCanvasFilled(cvs){
    var width = cvs.width;
    var height = cvs.height;

    var ctx = cvs.getContext("2d");
    var backgroundColor = [0, 0, 0, 0];
    var fillColor = [75, 209, 135, 255];
    var img_data = ctx.getImageData(0, 0, width, height).data;

    var idx = 0
    var pix = [];
    var refColor = backgroundColor;
    var chunk = [];
    var filled = [];

    for(var x = 0; x < width; ++x){
        idx = x * 4;
        pix = img_data.slice(idx, idx + 4);

        if(arraysEqual(pix, backgroundColor) && arraysEqual(refColor, fillColor)){
            chunk[1] = x / width;
            filled.push(chunk);
            chunk = [];
            refColor = backgroundColor;
        }
        else if(arraysEqual(pix, fillColor) && arraysEqual(refColor, backgroundColor)){
            chunk[0] = x / width;
            refColor = fillColor;
        }

        for(var y = 1; y < height; ++y){
            idx = (x + y * width) * 4;
            pix = img_data.slice(idx, idx + 4);
//            if(!arraysEqual(pix, refColor)) return false;
        }
    }
    if(arraysEqual(refColor, fillColor)){
        chunk[1] = 1;
        filled.push(chunk);
    }

    return filled;
}

return isCanvasFilled(arguments[0]);
"""

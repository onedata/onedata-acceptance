"""Utils and fixtures to facilitate operations on various web elements in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial
from selenium.webdriver.common.by import By

from .base import AbstractWebElement, AbstractWebItem
from .web_objects import (ButtonPageObject, PageObjectsSequence,
                          ButtonWithTextPageObject)
from tests.gui.utils.generic import find_web_elem, find_web_elem_with_text
from tests.utils.utils import repeat_failed


class WebElement(AbstractWebElement):
    def __init__(self, *args, **kwargs):
        self.parent_name = kwargs.pop('parent_name', '')
        super(WebElement, self).__init__(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return find_web_elem(instance.web_elem, self.css_sel,
                             lambda: self._format_msg('no {item} item found '
                                                      'in {parent}', instance))

    def _format_msg(self, err_msg, parent, **kwargs):
        name = self.name.replace('_', ' ').strip().upper()
        p_name = (self.parent_name if self.parent_name != '' else str(parent))
        return err_msg.format(item=name, parent=p_name, **kwargs)


class WebElementWithText(WebElement):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text', None)
        if self.text is None:
            raise ValueError('text not specified')
        super(WebElementWithText, self).__init__(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        err_msg = 'no {item} with "{text}" text found in {parent}'
        return find_web_elem_with_text(instance.web_elem,
                                       self.css_sel, self.text,
                                       lambda: self._format_msg(err_msg, instance,
                                                                text=self.text))


class WebItem(AbstractWebItem, WebElement):
    def __get__(self, instance, owner):
        elem = super(WebItem, self).__get__(instance, owner)
        return elem if instance is None else self.cls(instance.driver,
                                                      elem, parent=instance,
                                                      name=self.name)


class WebItemWithText(WebItem, WebElementWithText):
    pass


Button = partial(WebItem, cls=ButtonPageObject)
NamedButton = partial(WebItemWithText, cls=ButtonWithTextPageObject)


class Label(WebElement):
    item_not_found_msg = '{item} label not found in {parent}'

    def __get__(self, instance, owner):
        item = super(Label, self).__get__(instance, owner)
        return item.text if instance else item


class Input(WebElement):
    def __get__(self, instance, owner):
        item = super(Input, self).__get__(instance, owner)
        return item.get_attribute('value') if instance else item

    def __set__(self, instance, val):
        input_box = super(Input, self).__get__(instance, type(instance))
        input_box.clear()
        if val != '':
            input_box.send_keys(val)
            assert input_box.get_attribute('value') == val, \
                'entering "{}" to {} in {} failed'.format(val, self.name,
                                                          instance)


class AceEditor(WebElement):
    def __get__(self, instance, owner):
        selector = self.css_sel + ' .ace_content'
        script = (f"var textarea = document.querySelector('{selector}');"
                  f"return textarea")
        driver = instance.web_elem.parent
        return driver.execute_script(script).text

    def __set__(self, instance, val):
        driver = instance.web_elem.parent
        selector = self.css_sel + ' .ace_text-input'
        script = (f"var textarea = document.querySelector('{selector}');"
                  f"textarea.value = '{val}';"
                  "textarea.dispatchEvent(new Event('input', { bubbles: true}));"
                  "return textarea.value")
        inserted_val = driver.execute_script(script)
        msg = f'Inserted val is {inserted_val} instead of {val}'
        assert val == inserted_val, msg


class WebElementsSequence(AbstractWebElement):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.web_elem.find_elements(By.CSS_SELECTOR, self.css_sel)


class WebItemsSequence(AbstractWebItem, WebElementsSequence):
    def __get__(self, instance, owner):
        seq = super(WebItemsSequence, self).__get__(instance, owner)
        return seq if instance is None else PageObjectsSequence(instance.driver,
                                                                seq, self.cls,
                                                                instance)


class Icon(WebElement):
    item_not_found_msg = '{item} icon not found in {parent}'

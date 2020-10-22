"""Utils to facilitate spaces operations in op panel GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import re

from selenium.webdriver import ActionChains

from tests.gui.utils.common.common import Toggle, DropdownSelector
from tests.gui.utils.core.base import PageObject, ExpandableMixin
from tests.gui.utils.core.web_elements import (Label, NamedButton, Button,
                                               Input, WebItem, WebElement,
                                               WebItemsSequence,
                                               WebElementsSequence)
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject

DEFAULT_IMPORT_STRATEGY_CONFIG = {'Mode': 'auto',
                                  'Max depth': '65535',
                                  'Synchronize ACL': 'false',
                                  'Detect modifications': 'true',
                                  'Detect deletions': 'true',
                                  'Continuous scan': 'true',
                                  'Scan interval [s]': '60'
                                  }


class StorageImportConfiguration(PageObject):
    modes = WebItemsSequence('.field-mode-mode label.clickable',
                             cls=ButtonWithTextPageObject)
    max_depth = Input('.field-generic-maxDepth')
    synchronize_acl = Toggle('.toggle-field-generic-syncAcl')
    detect_modifications = Toggle('.toggle-field-generic-detectModifications')
    detect_deletions = Toggle('.toggle-field-generic-detectDeletions')
    continuous_scan = Toggle('.toggle-field-generic-continuousScan')
    scan_interval = Input('.field-continuous-scanInterval')

    def is_toggle_checked(self, toggle):
        toggle = getattr(self, toggle)
        return toggle.is_checked()


class SpaceSupportForm(PageObject):
    storage_selector = DropdownSelector('.ember-basic-dropdown')
    token = Input('input.field-main-token')
    size = Input('input.field-main-size')
    units = WebItemsSequence('.field-main-sizeUnit label.clickable',
                             cls=ButtonWithTextPageObject)
    import_storage_data = Toggle('.toggle-field-main-importEnabled')

    storage_import_configuration = WebItem('.import-configuration-section',
                                           cls=StorageImportConfiguration)

    support_space = Button('.btn.ready')


class SpaceInfo(PageObject):
    space_name = Label('.space-name')
    space_id = Input('.space-info .content-row:nth-child(2) input[type=text]')
    storage_name = Label('.space-provider-storage')
    _storage_import = WebElement('.storage-import')
    size = Input('.size-number-input')

    @property
    def import_strategy(self):
        values = DEFAULT_IMPORT_STRATEGY_CONFIG.copy()
        values.update(self._get_labels(self._storage_import))
        return values

    @staticmethod
    def _get_labels(elem):
        items = elem.find_elements_by_css_selector('strong, .one-label')
        items.pop(0)  # pop redundant "Storage import:" label
        return {attr.text.strip(':'): val.text for attr, val
                in zip(items[::2], items[1::2])}


class SyncChart(PageObject):
    configure = NamedButton('button', text='Configure')
    settings = Button('.oneicon-settings')

    storage_import_configuration = WebItem('.storage-import-update-form '
                                           '.import-configuration-section',
                                           cls=StorageImportConfiguration)
    auto_import_scan = WebElement('.import-info-header')
    start_scan = NamedButton('button', text='Start scan')

    last_minute_view = Button('.btn-import-interval-minute')
    last_hour_view = Button('.btn-import-interval-hour')
    last_day_view = Button('.btn-import-interval-day')

    save_configuration = Button('.btn-primary')

    _inserted = WebElementsSequence('.storage-import-chart-operations '
                                    'g.ct-series-0 line')
    _updated = WebElementsSequence('.storage-import-chart-operations '
                                   'g.ct-series-1 line')
    _deleted = WebElementsSequence('.storage-import-chart-operations '
                                   'g.ct-series-2 line')

    @property
    def inserted(self):
        return self._get_chart_bar_values(self._inserted)

    @property
    def updated(self):
        return self._get_chart_bar_values(self._updated)

    @property
    def deleted(self):
        return self._get_chart_bar_values(self._deleted)

    @staticmethod
    def _get_chart_bar_values(bars):
        return sum(int(bar.get_attribute('ct:value')) for bar in bars)


class FilePopularity(PageObject):
    enable_file_popularity = Toggle('.one-way-toggle-control')

    lastOpenHourWeightGroup = Input('.lastOpenHourWeightGroup input')
    avgOpenCountPerDayWeightGroup = Input('.avgOpenCountPerDayWeightGroup '
                                          'input')
    maxAvgOpenCountPerDayGroup = Input('.maxAvgOpenCountPerDayGroup input')


class QuotaEditor(PageObject):
    edit_button = Button('.oneicon-rename')
    edit_input = WebElement('input')
    accept_button = Button('.oneicon-checked')
    cancel_button = Button('.oneicon-ban-left')


class CleaningReport(PageObject):
    start = WebElement('td.data-cell-start')
    stop = WebElement('td.data-cell-stop')
    released_size = WebElement('td.data-cell-released-size')
    files_number = WebElement('td.data-cell-files-number')
    status = WebElement('td.data-cell-status')


class SelectiveCleaningRecord(PageObject):
    name = id = Label('.label-column.control-label')
    checkbox = Toggle('.toggle-column')
    value_input = Input('.condition-number-input')
    dropdown_button = Button('.ember-power-select-trigger')
    dropdown = WebItemsSequence('li.ember-power-select-option',
                                cls=ButtonWithTextPageObject)


class AutoCleaning(PageObject):
    enable_auto_cleaning = Toggle('.cleaning-enabled-toggle '
                                  '.one-way-toggle-control')
    selective_cleaning = Toggle('.selective-cleaning-toggle '
                                '.one-way-toggle-control')
    selective_cleaning_form = WebItemsSequence('.selective-cleaning-rules-form '
                                               '> div',
                                               cls=SelectiveCleaningRecord)

    start_cleaning_now = Button('.btn-clean-now')

    _soft_quota = WebElement('.soft-quota-editor')
    soft_quota = WebItem('.soft-quota-editor', cls=QuotaEditor)
    _hard_quota = WebElement('.hard-quota-editor')
    hard_quota = WebItem('.hard-quota-editor', cls=QuotaEditor)

    cleaning_reports = WebItemsSequence('tbody tr.data-item-base',
                                        cls=CleaningReport)

    def click_rename_soft_quota_button(self, driver):
        ActionChains(driver).move_to_element(self._soft_quota).perform()
        self.soft_quota.edit_button()

    def click_rename_hard_quota_button(self, driver):
        ActionChains(driver).move_to_element(self._hard_quota).perform()
        self.hard_quota.edit_button()


class NavigationHeader(PageObject):
    overview = NamedButton('li', text='Overview')
    storage_import = NamedButton('li', text='Storage import')
    file_popularity = NamedButton('li', text='File popularity')
    auto_cleaning = NamedButton('li', text='Auto-cleaning')


class SpaceRecord(PageObject, ExpandableMixin):
    name = id = Label('.item-icon-container + .one-label .item-name')
    toolbar = Button('.collapsible-toolbar-toggle')

    _toolbar = WebElement('.one-collapsible-toolbar')
    _toggle = WebElement('.one-collapsible-list-item-header')

    def is_expanded(self):
        return bool(re.match(r'.*\b(?<!-)opened\b.*',
                             self._toggle.get_attribute('class')))

    def expand_menu(self, driver):
        ActionChains(driver).move_to_element(self._toolbar).perform()
        self.toolbar.click()


class Space(PageObject):
    toolbar = Button('.collapsible-toolbar-toggle')
    navigation = WebItem('.space-tabs ul.nav-tabs', cls=NavigationHeader)

    overview = WebItem('.tab-pane.active', cls=SpaceInfo)
    sync_chart = WebItem('.tab-pane.active', cls=SyncChart)
    file_popularity = WebItem('.tab-pane.active', cls=FilePopularity)
    auto_cleaning = WebItem('.tab-pane.active', cls=AutoCleaning)


class SpacesContentPage(PageObject):
    spaces = WebItemsSequence('ul.one-collapsible-list '
                              '.cluster-spaces-table-item', cls=SpaceRecord)
    support_space = NamedButton('.btn-support-space', text='Support space')
    form = WebItem('.form-title~.ember-view>[role="form"]',
                   cls=SpaceSupportForm)
    cancel_supporting_space = NamedButton('.btn-support-space',
                                          text='Cancel supporting space')
    space = WebItem('.content-clusters-spaces', cls=Space)

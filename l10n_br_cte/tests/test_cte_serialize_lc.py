# @ 2020 KMEE INFORMATICA LTDA - www.kmee.com.br -
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from .test_cte_serialize import TestCTeSerialize

_logger = logging.getLogger(__name__)


class TestCTeExportLC(TestCTeSerialize):
    def setUp(self):
        cte_list = [
            {
                "record_ref": "l10n_br_cte.demo_cte_lc_modal_ferroviario",
                "xml_file": "CTe35230905472475000102580200000602011208018449.xml",
            },
            {
                "record_ref": "l10n_br_cte.demo_cte_lc_modal_rodoviario",
                "xml_file": "CTe35230905472475000102580200000602071611554500.xml",
            },
        ]
        super().setUp(cte_list)

    def test_serialize_xml(self):
        for cte_data in self.cte_list:
            diff = self.serialize_xml(cte_data)
            _logger.info("Diff with expected XML (if any): %s" % (diff,))
            assert len(diff) == 0

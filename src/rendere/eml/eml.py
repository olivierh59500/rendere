#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: eml

:Synopsis:

:Author:
    servilla

:Created:
    3/19/20
"""
import daiquiri
from lxml import etree

from rendere.eml.eml_dataset import eml_dataset
from rendere.eml.eml_resource import eml_resource
from rendere.eml.eml_responsible_party import eml_responsible_party

logger = daiquiri.getLogger(__name__)


class Eml:
    def __init__(self, eml_root):
        self._eml_root = eml_root
        self._package_id = (self._eml_root.attrib["packageId"]).strip()
        self._version = ((self._eml_root.nsmap["eml"]).split("/"))[-1]
        for module_type in ["dataset", "citation", "software", "protocol"]:
            module = eml_root.find(f"./{module_type}")
            if module is not None:
                break
        if module_type == "dataset":
            self._eml_dataset = eml_dataset(module)
        else:
            msg = f"Not supported module type: {module_type}"
            raise ValueError(msg)

    @property
    def dataset(self):
        return self._eml_dataset

    @property
    def package_id(self):
        return self._package_id

    @property
    def version(self):
        return self._version


class Eml210(Eml):
    def __init__(self, eml_root):
        super().__init__(eml_root)


class Eml211(Eml):
    def __init__(self, eml_root):
        super().__init__(eml_root)


class Eml220(Eml):
    def __init__(self, eml_root):
        super().__init__(eml_root)


versions = {
        "eml://ecoinformatics.org/eml-2.1.0": Eml210,
        "eml://ecoinformatics.org/eml-2.1.1": Eml211,
        "https://eml.ecoinformatics.org/eml-2.2.0": Eml220,
}


def eml_factory(eml_str: str):
    """
    Returns the EML object for the specified version of EML
    :param eml_str: EML XML string
    :return: EML object
    """
    eml = eml_str.encode("utf-8")
    eml_root = etree.fromstring(eml)
    return versions[eml_root.nsmap["eml"]](eml_root)


def main():
    return 0


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
# This file is a part of Anyblok / Wms Base project
#
#    Copyright (C) 2018 Georges Racinet <gracinet@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

import sys
import logging
from datetime import datetime

import anyblok
from anyblok.blok import Blok

logger = logging.getLogger(__name__)


def import_declarations(reload=None):
    pass


class WmsDemo(Blok):
    """Blok giving the structure for the code examples or live demonstration.
    """
    version = '0.2.0'
    author = "Georges Racinet"
    required = ['wms-core']

    def install(self):
        Initializer(self.registry).init_all()

    def update(self, latest_version):
        if latest_version is None:
            self.install()

    @classmethod
    def import_declaration_module(cls):
        import_declarations()

    @classmethod
    def reload_declaration_module(cls, reload):
        import_declarations(reload=reload)


class Initializer:

    def __init__(self, registry):
        self.registry = registry
        self.now = datetime.now()
        self.Wms = registry.Wms
        self.PhysObj = registry.Wms.PhysObj
        self.Avatar = self.PhysObj.Avatar
        self.POT = self.PhysObj.Type

        self.Operation = registry.Wms.Operation
        self.Apparition = self.Operation.Apparition
        self.Arrival = self.Operation.Arrival
        self.Move = self.Operation.Move

    def arrival(self, goods_code, loc_code, state='done', props=None):
        return self.Arrival.create(
            state=state,
            goods_type=self.POT.query().filter_by(code=goods_code).one(),
            location=self.PhysObj.query().filter_by(code=loc_code).one(),
            goods_properties=props,
            )

    def move(self, avatar, loc_code, state='done'):
        return self.Move.create(
            input=avatar,
            destination=self.PhysObj.query().filter_by(code=loc_code).one(),
            state=state)

    def add_goods(self):
        for _ in range(5):
            arr = self.arrival("GR-DUST-WIND-VOL2", "QUAI ENTRÉE",
                               props=dict(lot="12A345"))
            move = self.move(arr.outcomes[0], 'CASIER3')
            move2 = self.move(move.outcomes[0], 'EMBALLAGE')
            self.move(move2.outcomes[0], 'QUAI SORTIE', state='planned')
        self.arrival("GR-DUST-WIND-VOL1/PALETTE", "SALLE1")

    def add_data(self):
        self.add_goods()

    def init_all(self):
        self.init_locations()
        self.init_types()

    def init_types(self):
        livre = self.POT.insert(code="LIVRE")
        bois_pal = self.POT.insert(code="PALETTE SUPPORT")
        dust_wind = self.POT.insert(code="GR-DUST-WIND", parent=livre)
        for vol in (1, 2, 3):
            prod = "GR-DUST-WIND-VOL%d" % vol
            book = self.POT.insert(code=prod, parent=dust_wind)
            cardboard = self.POT.insert(
                code=prod + "/CARTON",
                parent=dust_wind,
                behaviours=dict(unpack=dict(
                    outcomes=[
                        dict(type=book.code,
                             quantity=50,
                             forward_properties=['lot'])
                        ]
                )))
            self.POT.insert(code=prod + "/PALETTE",
                            parent=dust_wind,
                            behaviours=dict(unpack=dict(
                                outcomes=[
                                    dict(type=cardboard.code,
                                         quantity=80,
                                         forward_properties=['lot']),
                                    dict(type=bois_pal.code,
                                         quantity=1)
                                    ]
                            )))

    def init_locations(self):
        fixed_loctype = self.POT.insert(code='EMPLACEMENT FIXE',
                                        behaviours=dict(container=True)
                                        )
        wh = self.Wms.create_root_container(fixed_loctype, code='ENTR')
        for code in ('QUAI ENTRÉE', 'STOCK', 'QUAI SORTIE', "EMBALLAGE"):
            self.Apparition.create(goods_type=fixed_loctype,
                                   location=wh,
                                   state='done',
                                   quantity=1,
                                   goods_code=code,
                                   )

        stock = self.PhysObj.query().filter_by(code='STOCK').one()
        for code in ('SALLE1', 'SALLE2', 'SALLE3'):
            self.Apparition.create(goods_type=fixed_loctype,
                                   quantity=1,
                                   goods_code=code,
                                   state='done',
                                   location=stock)

        salle = self.PhysObj.query().filter_by(code='SALLE2').one()
        for code in ('ARMOIRE1', 'ARMOIRE2', 'ARMOIRE3'):
            self.Apparition.create(goods_type=fixed_loctype,
                                   state='done',
                                   quantity=1,
                                   goods_code=code,
                                   location=salle)

        armoire = self.PhysObj.query().filter_by(code='ARMOIRE1').one()
        for code in ('CASIER1', 'CASIER2', 'CASIER3'):
            self.Apparition.create(goods_type=fixed_loctype,
                                   state='done',
                                   quantity=1,
                                   goods_code=code,
                                   location=armoire)


def add():
    """Add more data to the example DB.

    This was merely useful to prepare incrementally the example.
    """
    registry = anyblok.start('basic', configuration_groups=[],
                             loadwithoutmigration=True,
                             isolation_level='SERIALIZABLE')
    if registry is None:
        logging.critical("Couldn't initialize registry")
        sys.exit(1)

    init = Initializer(registry)
    try:
        init.add_data()
    except:
        import pdb
        pdb.post_mortem(sys.exc_info()[2])
        registry.rollback()
        raise
    import pdb; pdb.set_trace()
    registry.commit()
    registry.close()

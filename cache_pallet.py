"""
pallet for updating the caching databases
"""

import arcpy
import settings
from forklift.models import Pallet


class CachePallet(Pallet):
    def build(self, config):
        self.sgid = r'C:\Cache\MapData\SGID10.sde'
        self.sgid_local = r'C:\Cache\MapData\SGID10_WGS.gdb'
        self.basemapdata = r'C:\Cache\MapData\SGID10_WGS.gdb'
        self.sgid_network_drive = settings.HNAS + r'\BaseMaps\Data\SGID10_WGS.gdb'
        self.basemapdata_remote = settings.HNAS + r'\BaseMaps\Data\UtahBaseMap-Data_WGS.gdb'

        self.copy_data = []

        self.log.info('adding crates for {} (local & remote)'.format(self.sgid_local.split('\\')[-1]))
        arcpy.env.workspace = self.sgid_network_drive
        for feature_class in arcpy.ListFeatureClasses():
            self.log.info(feature_class)

            self.add_crate((feature_class, self.sgid, self.sgid_local))
            self.add_crate((feature_class, self.sgid, self.sgid_network_drive))

        arcpy.env.workspace = self.basemapdata_remote
        self.log.info('adding crates for {}'.format(self.basemapdata.split('\\')[-1]))
        for feature_class in arcpy.ListFeatureClasses():
            self.log.info(feature_class)

            self.add_crate((feature_class, self.basemapdata_remote, self.basemapdata))
        arcpy.env.workspace = None

    def process(self):
        for database in [self.sgid_local, self.sgid_network_drive, self.basemapdata_remote, self.basemapdata]:
            self.log.info('compacting {}'.format(database))
            arcpy.Compact_management(database)

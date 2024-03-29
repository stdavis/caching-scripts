import arcpy
from os.path import join

LOCAL = r'C:\Cache\MapData'
HNAS = r'\\grhnas01sp.state.ut.us\BaseMaps\Data'
SGID = join(HNAS, 'SGID10.sde')
SGID_GDB_NAME = 'SGID10_WGS.gdb'


def main():
    print('getting SGID fc lookup')
    sgid_fcs = {}
    arcpy.env.workspace = SGID
    for fc in arcpy.ListFeatureClasses():
        sgid_fcs[fc.split('.')[-1]] = fc

    print('updating SGID data on HNAS')
    arcpy.env.workspace = join(HNAS, SGID_GDB_NAME)
    for fc in arcpy.ListFeatureClasses():
        print(fc)
        arcpy.Delete_management(fc)
        arcpy.Project_management(join(SGID, sgid_fcs[fc]), fc, arcpy.SpatialReference(3857), 'NAD_1983_To_WGS_1984_5')

    print('copying databases locally')
    for db in [SGID_GDB_NAME, 'UtahBaseMap-Data_WGS.gdb']:
        local_db = join(LOCAL, db)
        hnas_db = join(HNAS, db)
        arcpy.management.Delete(local_db)
        arcpy.management.Copy(join(HNAS, db), join(LOCAL, db))

    arcpy.env.workspace = None


if __name__ == '__main__':
    main()
    print('done')

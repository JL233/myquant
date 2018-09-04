from kdata import const
from service.kdata_srv.kdata_srv import KdataThread

if __name__ == '__main__':
    KdataThread("000001", const.BAR_ASSET_INDEX, "D").start()
    KdataThread("000001", const.BAR_ASSET_INDEX, "60min").start()
    KdataThread("000001", const.BAR_ASSET_INDEX, "30min").start()
    KdataThread("000001", const.BAR_ASSET_INDEX, "15min").start()
    KdataThread("000001", const.BAR_ASSET_INDEX, "5min").start()
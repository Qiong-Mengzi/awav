'''
加载assets文件夹的资源文件
'''

from readerwriterlock import rwlock
from sys import getsizeof

ASSETS_PATH = 'assets'
ASSETS_CACHE: dict[str, bytes] = {}
AssetsCacheLock = rwlock.RWLockReadD()

def LoadAssets(res_id: str, ext: str, force: bool = False):
    '''
    加载数据，加载失败需自行处理异常`

    [In] res_id 资源id，路径分隔符使用`.`

    [In] ext 资源后缀名，必须加`.`

    [In] force 强制加载标志，如果为 `True`，则重新加载该资源
    '''
    if force:
        with AssetsCacheLock.gen_wlock():
            res_path = res_id.replace('.', '/') + ext
            with open(res_path, 'rb') as f:
                _tmp_res = f.read()
                ASSETS_CACHE[res_id] = _tmp_res
                return _tmp_res
    else:
        if res_id in ASSETS_CACHE:
            with AssetsCacheLock.gen_rlock():
                return ASSETS_CACHE[res_id]
        else:
            with AssetsCacheLock.gen_wlock():
                res_path = res_id.replace('.', '/') + ext
                with open(res_path, 'rb') as f:
                    _tmp_res = f.read()
                    ASSETS_CACHE[res_id] = _tmp_res
                    return _tmp_res

def GetAssetsCacheSize():
    with AssetsCacheLock.gen_rlock():
        total: int = getsizeof(ASSETS_CACHE)
        for k, v in ASSETS_CACHE.items():
            total += getsizeof(k) + getsizeof(v)
        return total

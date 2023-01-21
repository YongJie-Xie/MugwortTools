#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-01-13 14:26
@Description : 地理信息处理工具
@FileName    : geography
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import csv
import io
import os
import shutil
import tempfile
import typing as t
import urllib.request
import zipfile

from mugwort import Logger

try:
    from scipy.spatial import KDTree
except ImportError:
    raise ImportError(
        'Tool `data.geography` cannot be imported.',
        'Please execute `pip install mugwort[data-geography]` to install dependencies first.'
    )

__all__ = [
    'Coordinate2City',
]

CoordinateType = t.Tuple[t.Union[float, int], t.Union[float, int]]


class Coordinate2City:
    """
    经纬度转城市信息

    部分代码参考 https://github.com/thampiman/reverse-geocoder 项目
    """
    _rg_columns = ('lat', 'lon', 'name', 'admin1', 'admin2', 'cc')
    _gn_cities_columns = {
        'geoNameId': 0, 'name': 1, 'asciiName': 2, 'alternateNames': 3, 'latitude': 4, 'longitude': 5,
        'featureClass': 6, 'featureCode': 7, 'countryCode': 8, 'cc2': 9, 'admin1Code': 10, 'admin2Code': 11,
        'admin3Code': 12, 'admin4Code': 13, 'population': 14, 'elevation': 15, 'dem': 16, 'timezone': 17,
        'modificationDate': 18,
    }
    _gn_admin_columns = {'concatCodes': 0, 'name': 1, 'asciiName': 2, 'geoNameId': 3}

    def __init__(
            self,
            rg_filepath: str = 'rg_cities500.csv',
            gn_download_switch: bool = True,
            gn_download_cities: t.Literal['cities500', 'cities1000', 'cities5000', 'cities15000'] = 'cities500',
            logger: t.Optional[Logger] = None,
    ):
        """
        初始化 reverse_geocoder 工具

        :param rg_filepath: 符合 reverse_geocoder 要求的数据源
        :param gn_download_switch: 从 GeoNames 组织下载数据的开关
        :param gn_download_cities: 从 GeoNames 组织下载数据的类型
        :param logger: 日志类
        """
        self._logger = logger or Logger('Coordinate2City')

        if gn_download_cities not in ['cities500', 'cities1000', 'cities5000', 'cities15000']:
            raise ValueError('无效的 gn_download_cities 参数')

        if not os.path.exists(rg_filepath) and gn_download_switch:
            self._geonames_download(rg_filepath, gn_download_cities)

        if not os.path.exists(rg_filepath):
            raise RuntimeError('没有可用的数据源')

        with open(rg_filepath, encoding='utf-8') as file:
            stream = io.StringIO(file.read())

        coordinates, self._locations = self._reverse_geocoder_load(stream)
        self._tree = KDTree(coordinates)

    def get_city(self, coordinate: CoordinateType) -> dict:
        """
        根据经纬度获取城市信息

        :param coordinate: 经纬度（经度、纬度）
        :return: 经纬度对应的城市信息
        """
        _, indices = self._tree.query([(lat, lon) for lon, lat in [coordinate]], k=1)
        return self._locations[indices[0]]

    def get_cities(self, coordinates: t.List[CoordinateType]) -> t.Dict[CoordinateType, dict]:
        """
        根据经纬度批量获取城市信息

        :param coordinates: 包含经纬度（经度、纬度）的列表
        :return: 各个经纬度对应的城市信息
        """
        _, indices = self._tree.query([(lat, lon) for lon, lat in coordinates], k=1)
        return dict(zip(coordinates, [self._locations[index] for index in indices]))

    def _geonames_download(self, save_filepath: str, gn_cities: str):
        """
        下载 GeoNames 组织提供的数据源

        :param save_filepath: 保存位置
        :param gn_cities: 下载的数据类型
        """
        base_url = 'https://download.geonames.org/export/dump/'

        gn_cities_zip = gn_cities + '.zip'
        gn_cities_txt = gn_cities + '.txt'
        gn_admin1_txt = 'admin1CodesASCII.txt'
        gn_admin2_txt = 'admin2Codes.txt'

        with tempfile.TemporaryDirectory() as temp_folder:
            try:
                self._logger.info('创建临时目录...')
                gn_cities_zip_filepath = os.path.join(temp_folder, gn_cities_zip)
                gn_cities_txt_filepath = os.path.join(temp_folder, gn_cities_txt)
                gn_admin1_txt_filepath = os.path.join(temp_folder, gn_admin1_txt)
                gn_admin2_txt_filepath = os.path.join(temp_folder, gn_admin2_txt)

                self._logger.info('下载数据文件...')
                urllib.request.urlretrieve(base_url + gn_cities_zip, gn_cities_zip_filepath)
                urllib.request.urlretrieve(base_url + gn_admin1_txt, gn_admin1_txt_filepath)
                urllib.request.urlretrieve(base_url + gn_admin2_txt, gn_admin2_txt_filepath)

                self._logger.info('提取城市信息...')
                with (
                    zipfile.ZipFile(open(gn_cities_zip_filepath, 'rb')) as gn_cities_zip_file,
                    open(gn_cities_txt_filepath, 'wb') as gn_cities_txt_file,
                ):
                    gn_cities_txt_file.write(gn_cities_zip_file.read(gn_cities_txt))

                self._logger.info('读取数据文件...')
                with (
                    open(gn_cities_txt_filepath, 'rt', encoding='utf8') as gn_cities_txt_file,
                    open(gn_admin1_txt_filepath, 'rt', encoding='utf8') as gn_admin1_txt_file,
                    open(gn_admin2_txt_filepath, 'rt', encoding='utf8') as gn_admin2_txt_file,
                ):
                    gn_cities_rows = [
                        row for row in csv.reader(gn_cities_txt_file, delimiter='\t', quoting=csv.QUOTE_NONE)
                    ]
                    gn_admin1_rows = [row for row in csv.reader(gn_admin1_txt_file, delimiter='\t')]
                    gn_admin2_rows = [row for row in csv.reader(gn_admin2_txt_file, delimiter='\t')]

                rows = self._geonames_extract(gn_cities_rows, gn_admin1_rows, gn_admin2_rows)
            finally:
                self._logger.info('删除临时目录...')
                shutil.rmtree(temp_folder)

        self._logger.info('保存地理编码文件...')
        with open(save_filepath, 'wt', encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._rg_columns)
            writer.writeheader()
            writer.writerows(rows)

    def _geonames_extract(
            self,
            cities_rows: t.List[t.List[str]],
            admin1_rows: t.List[t.List[str]],
            admin2_rows: t.List[t.List[str]],
    ) -> t.List[dict]:
        """
        将 GeoNames 组织下载的数据源处理成 reverse_geocoder 要求的数据格式

        :param cities_rows: 城市数据
        :param admin1_rows: 一级行政部门数据
        :param admin2_rows: 二级行政部门数据
        :return: 符合格式要求的数据
        """

        self._logger.info('加载一级行政区域代码...')
        admin1_map = {}
        for row in admin1_rows:
            admin1_map[row[self._gn_admin_columns['concatCodes']]] = row[self._gn_admin_columns['asciiName']]

        self._logger.info('加载二级行政区域代码...')
        admin2_map = {}
        for row in admin2_rows:
            admin2_map[row[self._gn_admin_columns['concatCodes']]] = row[self._gn_admin_columns['asciiName']]

        self._logger.info('创建地理编码文件...')
        rows = []
        for row in cities_rows:
            lat, lon, name, cc = (
                row[self._gn_cities_columns['latitude']], row[self._gn_cities_columns['longitude']],
                row[self._gn_cities_columns['asciiName']], row[self._gn_cities_columns['countryCode']],
            )
            cc_admin1 = cc + '.' + row[self._gn_cities_columns['admin1Code']]
            cc_admin2 = cc_admin1 + '.' + row[self._gn_cities_columns['admin2Code']]
            admin1 = admin1_map[cc_admin1] if cc_admin1 in admin1_map else ''
            admin2 = admin2_map[cc_admin2] if cc_admin2 in admin2_map else ''
            rows.append({'lat': lat, 'lon': lon, 'name': name, 'admin1': admin1, 'admin2': admin2, 'cc': cc})

        return rows

    def _reverse_geocoder_load(self, stream: io.StringIO) -> t.Tuple[t.List[CoordinateType], t.List[dict]]:
        stream_reader = csv.DictReader(stream, delimiter=',')

        if tuple(stream_reader.fieldnames) != self._rg_columns:
            raise csv.Error('输入必须是以逗号分隔且标题包含 %s 列的文件' % (','.join(self._rg_columns)))

        self._logger.info('加载地理编码文件...')
        geo_coords: t.List[CoordinateType] = []
        locations: t.List[dict] = []
        for row in stream_reader:
            geo_coords.append((row['lat'], row['lon']))
            locations.append(row)

        return geo_coords, locations

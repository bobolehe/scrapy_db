import logging
import datetime

# 实例化日志类
logger = logging.getLogger(__name__)


def datestime(self, stime):
    """
    简单翻译爬取到的英语月份
    :param self:
    :param stime:
    :return:
    """
    date1 = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    date2 = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    stime = stime
    stime = stime.replace(',', '').split(' ')

    stime[1] = str(date2[stime[1]])
    stime = [stime[2], stime[1], stime[0]]
    return '-'.join(stime)


def VerificationData(self, Mdata, item, response):
    """

    :param self:
    :param Mdata:
    :param item:
    :param response:
    :return:
    """
    try:
        # 校验数据是否存在数据库
        err = Mdata.price_exists(field='groups_id', price=item['groups_id'])
        # 不存在数据库，直接进行存储
        if err['error'] == 101:
            item['pagemax'] = 1
            return item
        # 查询语句出错，返回信息，停止程序
        elif err['error'] == 104 or err['error'] == 103:
            logger.error(f'{response.url}数据查询失败：错误信息{err["log"]}')
            self.crawler.engine.close_spider(self, '数据库查询信息出错')

        # 查询数据库中已有数据的数据更新时间
        data_stime = Mdata.query_page(field=item['groups_id'], name='uptodate_time', fields='groups_id')[0]
        # 没有数据更新时间，再次进行存储
        if not data_stime:
            logger.error(f'{response.url}数据存在,但无更新日期，进行更新')
            item['pagemax'] = int(Mdata.query_page(field=item['groups_id'], name='pagemax', fields='groups_id')[0]) + 1
            return item
        # 存在更新时间与当前爬取到时间比较，是否需要数据存储
        date_obj = datetime.datetime.strptime(item['uptodate_time'], "%Y-%m-%d")
        # 有新的更新时间进行数据存储
        if data_stime < date_obj:
            logger.error(f'更新{response.url}数据')
            item['pagemax'] = int(Mdata.query_page(field=item['groups_id'], name='pagemax', fields='groups_id')[0]) + 1
            return item

    except Exception as e:
        logger.error(f"数据库校验数据失败，错误信息{e}")

# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

import time

# 64位ID的划分
from loguru import logger

from .exceptions import InvalidSystemClock

# id生成器
# 时间戳从2016-01-01开始计算
# work_id 7位，最大99
# 每秒最多产生4096个序号

WORKER_ID_BITS = 7
# DATACENTER_ID_BITS = 4
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = 99
# -1 ^ (-1 << WORKER_ID_BITS)  2**5-1 0b11111

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1451577600


class IdGenerator(object):
    """
    用于生成IDs
    """

    def __init__(self, worker_id):
        """
        初始化
        :param worker_id: 机器ID
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        self.worker_id = worker_id
        self.sequence = 0

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time())

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logger.error('Timestamp missing. now: {}, last_timestamp: {}', timestamp, self.last_timestamp)
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


if __name__ == '__main__':
    worker = IdGenerator(1)
    i = 0
    while i < 10000:
        print(worker.get_id())
        i += 1

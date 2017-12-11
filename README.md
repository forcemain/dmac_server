# dmac_server
#### 简单介绍:
>[dmac_server](https://github.com/xmdevops/dmac_server) 主要用于记录分析设备上报信息,兼容PY2.7+

***


#### 组件简介:
* UdpServer组件基于SocketServer库封装,统一入口支持阻塞/非阻塞(多线程/多进程)响应
* ORM组件按照django_orm思路实现了基础ORM(Mapping+Manager)
* Signal组件按照django_signal思路实现了完整Signal功能
* Geoip组件基于geoip2+openrestry_lua-geoip库封装,统一入口查询定位


#### 开发环境:
> SY_ENV: MacOS 10.12.6 \
> PY_ENV: Python2.7.10 

***

#### 快速启动:
`git clone https://github.com/xmdevops/dmac_server` \
`cd dmac_server` \
`python manage.py` 

***

### 使用方法:
```python
#! -*- coding: utf-8 -*-


from server.models import DmacCenter
from SocketServer import DatagramRequestHandler
from server.handlers.base_handler import BaseHandler


class MacUdpServerRequestHandler(DatagramRequestHandler, BaseHandler):
    def handle(self):
        resp = '0' * 18
        data = self.rfile.readline()
        dict_data = self.unpack(data)
        if not dict_data:
            return
        d_host, d_port = self.client_address
        dict_data.update({
            'd_host': d_host,
            'd_port': d_port,
            'd_area': self.get_device_area(d_host)
        })
        # orm warehousing test, record Asia_Taiwan device enc info.
        if dict_data['d_area'] and dict_data['d_area'].startswith('Asia_Taiwan'):
            filter_conditions = {
                'd_mac': dict_data['d_mac'],
                'd_uuid': dict_data['d_uuid'],
                'd_type': dict_data['d_type']
            }
            get_res = DmacCenter.objects.get(**filter_conditions)
            if get_res is None:
                DmacCenter.objects.create(**dict_data)
            else:
                print 'GetResult:', get_res, 'Ignore.'

        self.wfile.write(resp)
```

#### Copyright:
2017.12.11  (c) Limanman <xmdevops@vip.qq.com>


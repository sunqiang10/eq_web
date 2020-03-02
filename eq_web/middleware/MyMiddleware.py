import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import redis
from django.utils.deprecation import MiddlewareMixin
import logging
import json
from eq_web.model.eq_info import EqInfo
import threading
import django.db as django_db


class MyMiddleware(MiddlewareMixin):
    pass


chooseC = 0
mylock = threading.Lock()
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    # @register_job(scheduler, "interval", seconds=1)

    @register_job(scheduler, "cron", minute='30', max_instances=5, misfire_grace_time=5)
    def my_job():
        # 这里写你要执行的任务
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        mylock.acquire()
        try:
            if django_db:
                django_db.close_old_connections()
                print('关闭数据库连接')
            pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
            r = redis.Redis(connection_pool=pool)
            print('r.llen:crawler_ceic_redis:items', r.llen('crawler_ceic_redis:items'))
            for i in range(r.llen('crawler_ceic_redis:items')):
                item = r.lpop('crawler_ceic_redis:items')
                logging.info(item.decode('unicode_escape'))
                rs = json.loads(item.decode('unicode_escape'))
                eq = EqInfo(**rs)
                is_had_eq = EqInfo.objects.filter(Cata_id=eq.Cata_id)
                if not is_had_eq:
                    eq.save()
                    logging.info("eq.save(" + eq.Cata_id + ")")
            global chooseC
            if chooseC == 1:
                chooseC = 0
                r.lpush('ceic:start_urls', 'https://m.weibo.cn')
            else:
                chooseC = 1
                r.lpush('ceic:start_urls', 'http://news.ceic.ac.cn')

        except Exception as e1:
            logging.error(e1)
        finally:
            if django_db:
                django_db.close_old_connections()
                print('关闭数据库连接')
            mylock.release()


    my_job()
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()



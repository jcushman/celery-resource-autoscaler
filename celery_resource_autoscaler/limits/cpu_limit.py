import multiprocessing
import os

from celery.utils.log import get_logger


logger = get_logger(__name__)
debug, info, error = logger.debug, logger.info, logger.error


class CPULimit:
    def __init__(self, min_load=0.0, max_load=1.1):
        self.num_cpus = multiprocessing.cpu_count()
        self.min_load = min_load
        self.max_load = max_load

    def get_range(self, proc_count, req):
        cur_load = self._get_load()
        info("CPU load: %s" % cur_load)
        if cur_load > self.max_load:
            info("CPU limit: load average %s exceeds maximum %s. Requesting scale down." % (cur_load, self.max_load))
            return (None, proc_count-1)
        if cur_load < self.min_load:
            info("CPU limit: load average %s below minimum %s. Requesting scale up." % (cur_load, self.min_load))
            return (proc_count+1, None)
        return (None, None)

    def _get_load(self):
        load1min, load5min, load15min = os.getloadavg()
        return 1.0 * max(load1min, 0.001) / self.num_cpus

import re

from celery.utils.log import get_logger


logger = get_logger(__name__)
debug, info, error = logger.debug, logger.info, logger.error

class MemoryLimit:
    def __init__(self, min_memory=0.0, max_memory=1.0):
        self.min_memory = min_memory
        self.max_memory = max_memory

    def get_range(self, proc_count, req):
        used_mem = self._get_used_mem()
        if used_mem > self.max_memory:
            info("Memory limit: used memory %s exceeds maximum %s. Requesting scale down." % (used_mem, self.max_memory))
            return (None, proc_count-1)
        if used_mem < self.min_memory:
            info("Memory limit: used memory %s below minimum %s. Requesting scale up." % (used_mem, self.min_memory))
            return (proc_count+1, None)
        return (None, None)

    re_total = re.compile(r"MemTotal:\s+(?P<total>\d+)\s+kB")
    re_free = re.compile(r"MemFree:\s+(?P<free>\d+)\s+kB")
    def _get_used_mem(self):
        try:
            # Try using the cross platform method.
            import psutil
        except ImportError:
            # If not, make it work for most linux distros.
            with open('/proc/meminfo', 'rb') as f:
                mem = f.read()
            return 1.0 - (1.0 * int(self.re_free.search(mem).group("free")) /
                    int(self.re_total.search(mem).group("total")))
        else:
            return psutil.virtual_memory().percent / 100

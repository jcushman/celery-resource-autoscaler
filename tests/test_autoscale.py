from mock import Mock
from celery_resource_autoscaler import ResourceAutoscaler

def test_instantiate():
    worker = Mock()
    worker.app.conf = {}
    worker.app.conf['resource_limits'] = [
        {
            'class': 'celery_resource_autoscaler:MemoryLimit',
            'kwargs': {'max_memory': 0.8},
        },
        {
            'class': 'celery_resource_autoscaler:CPULimit',
            'kwargs': {'max_load': 1.1},
        },
    ]
    ra = ResourceAutoscaler(pool=None, max_concurrency=None, worker=worker)

    assert ra.resource_limits[0].max_memory == 0.8
    assert ra.resource_limits[1].max_load == 1.1
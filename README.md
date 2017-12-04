Overview
========

Celery plugin to autoscale based on available CPU, memory, or other system attributes.

Installation
============

    pip install celery-resource-autoscaler

Documentation
=============

Basic configuration
------------------- 

To configure:

    app = Celery()
    app.conf.worker_autoscaler = 'celery_resource_autoscaler:ResourceAutoscaler'
    app.conf.resource_limits = [
        {
            'class': 'celery_resource_autoscaler:MemoryLimit',
            'kwargs': {'max_memory': 0.8},
        },
        {
            'class': 'celery_resource_autoscaler:CPULimit',
            'kwargs': {'max_load': 1.1},
        },
    ]

Then run celery with `--autoscale` enabled:

    celery worker --autoscale=1000
    
Celery will now scale up to 1000 workers as needed, but will stop scaling if memory exceeds 80% or load per CPU exceeds 1.1.

Custom limits
------------- 

You can provide custom Limit objects. Limit objects should provide a `get_range()` function that returns the current
minimum and maximum allowed workers:

    class FooLimit:
        def __init__(self, min_foo=1, max_foo=10):
            self.min_foo = min_foo
            self.max_foo = max_foo
    
        def get_range(self, proc_count, req):
            current_foo_count = get_foo_count()
            if current_foo_count > self.max_foo:
                info("Foo limit: count %s exceeds maximum %s. Requesting scale down." % (current_foo_count, self.max_foo))
                return (None, proc_count-1)
            if cur_load < self.min_foo:
                info("Foo limit: count %s below minimum %s. Requesting scale up." % (current_foo_count, self.min_foo))
                return (proc_count+1, None)
            return (None, None)

You can then use your custom Limit object:

    app.conf.resource_limits = [
        {
            'class': 'foo_module:FooLimit',
            'kwargs': {'max_foo': 20},
        }
    ]

If you come up with useful generic Limit objects, pull requests are welcome! 

Credits
=======

Code for the CPU and memory limits was based on
[this pastebin](https://gist.github.com/speedplane/224eb551c51a74068011f4d776237513) from speedplane.

Development
===========

To run the all tests run:

    tox

To combine the coverage data from all the tox environments run:

    PYTEST_ADDOPTS=--cov-append tox

===
API
===

.. automodule:: bvggrabber.api


General Functions
=================

   .. autofunction:: compute_remaining


Base and Main Classes
=====================

   .. autoclass:: Departure
      :members: __init__, remaining, __eq__, __lt__, __str__

   .. autoclass:: QueryApi
      :members: call

   .. autoclass:: Response
      :members: __init__, merge, departures, error, json, state


Concrete Implementations
========================

   .. toctree::
      api.actual
      api.scheduled
      :maxdepth: 1

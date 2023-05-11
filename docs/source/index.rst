.. _Driver-Framework:

=========================
Platform Driver Framework
=========================

VOLTTRON drivers act as an interface between agents on the platform and a device. Drivers are special purpose agents
which are run as a greenlet in the Platform Driver process (typically agents are spawned as their own process).
Drivers implement a specific set of features for device communication and ensure uniform behaviors across different
devices and protocols.

Drivers are managed by the :ref:`Platform Driver Agent <Platform-Driver-Agent>`. The Platform Driver
instantiates individual drivers and facilitates communication with them. Driver instances are created when a new device
configuration is added to the configuration store. Each driver instance uses an Interface class corresponding to the
`driver_type` parameter in the device configuration file.  The Interface class is responsible for implementing the
communication paradigms of a device or protocol. For more information regarding the development of driver interfaces,
see :ref:`the driver development page <Driver-Development>`.

.. _Driver_Communication:

Device Communication
====================

Once configured, the Platform Driver periodically polls the device through the interface class for data. This
functionality is intentionally not user-facing. The Platform Driver iterates over the configured drivers and calls their
respective "scrape_all" methods. This will trigger the drivers to collect all configured point values from the device,
which are then published to the message bus under the `devices/<device_topic>/all` topic. "<device_topic>" will
conventionally have a form similar to "<campus>/<building>/<device>/<sub_device>", though this depends entirely
on its configuration.

Additionally, point values can be requested ad-hoc or set via RPC methods exposed by the Platform Driver and Actuator
agents. The Actuator Agent adds scheduling capabilities to prevent race conditions which might occur if multiple
devices try to simultaneously set values on the same device.

* To get an individual device point, the user agent should send an RPC call to the Platform Driver for ``get_point``,
  providing the point's corresponding topic. After the Platform Driver processes the request, communication happens very
  similarly to polling, but rather than an "all" publish, the data is returned via the Platform Driver to the requestor.

* To set a point on a device, the ``set_point`` method can be called on either the
:ref:`Platform Driver <Platform-Driver-Agent>` or the :ref:`Actuator <Actuator-Agent>` agents.

* If there is a possibility of conflicting commands being given to devices, it is recommended to use an
  :ref:`Actuator Agent <Actuator-Agent>` instead of making calls directly to the Platform Driver. The user agent sends
  an RPC request to the Actuator to schedule a reservation for exclusive control of the device. During that scheduled
  time the user agent may send set point requests which the actuator will forward to the Platform Driver. Agents
  without a reservation, however, would be denied the ability to write to it.

Typical Data Flow
-----------------

The below diagram demonstrates driver communication on the platform in a typical case.

.. image:: files/driver_flow.png

1. Platform agents and agents developed and/or installed by users communicate with the platform via pub/sub or JSON-RPC.
   Agents share data for a number of reasons including querying historians for data to use in control algorithms,
   fetching data from remote web APIs and monitoring.
2. A user agent which wants to request data ad-hoc sends a JSON-RPC request to the Platform Driver to `get_point`,
    asking the driver to fetch the most up-to-date point data for the topic provided.

    .. note::

       For periodic `scrape_all` data publishes, step 2 is not required.  The Platform Driver is configured to
       automatically collect all point data for a device on a regular interval and publish the data to the bus.

3. A user agent sends a request to the actuator to establish a schedule for sending device control signals, and during
   the scheduled time sends a `set_point` request to the Actuator.  Given that the control signal arrives during the
   scheduled period, the Actuator forwards the request to the Platform Driver.  If the control signal arrives outside
    the scheduled period or without an existing schedule, a LockError exception will be thrown.
4. The Platform Driver issues a `get_point`/`set_point` call to the Driver corresponding to the request it was sent.
5. The device driver uses the interface class it is configured for to send a data request or control signal to the
   device (i.e. the BACnet driver issues a `readProperty` request to the device).
6. The device returns a response indicating the current state.
7. The the response is forwarded to the requesting device.  In the case of a `scrape_all`, the device data is published
   to the message bus.


Special Case Drivers
--------------------

Some drivers require a different communication paradigm. One common alternative is shown in the diagram below:

.. image:: files/proxy_driver_flow.png

This example describes an alternative pattern wherein BACnet drivers communicate via a BACnet proxy agent to communicate
with end devices. This behavior is derived from the networking requirements of the BACnet specification. BACnet
communication in the network layer requires that only one path exist between BACnet devices on a network.
In this case, the BACnet Proxy Agent acts as a virtual BACnet device, and device drivers forward their requests to this
agent which then implements the BACnet communication (whereas the typical pattern would have devices communicate
directly with the device). There are many other situations which may require this paradigm to be adopted (such as
working with remote APIs with request limits), and it is up to the party implementing the driver to determine if this
pattern or another pattern may be the most appropriate implementation pattern for their respective use case.

.. note::

   Other requirements for driver communication patterns may exist, but on an individual basis.  Please refer to the
   documentation for the driver of interest for more about any atypical pattern that must be adhered to.


Installing the Fake Driver
**************************

The Fake Driver is included as a way to quickly see data published to the message bus in a format that mimics what a
real driver would produce.  This is a simple implementation of the VOLTTRON driver framework.

See :ref:`instructions for installing the fake driver <Fake-Driver-Install>`

To view data being published from the fake driver on the message bus, one can
:ref:`install the Listener Agent <Listener-Agent>` and read the VOLTTRON log file:

.. code-block:: bash

    cd <root volttron directory>
    tail -f volttron.log

.. toctree::
   :hidden:

   Platform Driver <platform-driver-agent>
   Actuator <external-docs/volttron-actuator/docs/source/index>
   Fake <external-docs/volttron-lib-fake-driver/docs/source/index>
   BACnet <external-docs/volttron-lib-bacnet-driver/docs/source/index>
   DNP3 <external-docs/volttron-lib-dnp3-driver/docs/source/index>
   Modbus <external-docs/volttron-lib-modbus-driver/docs/source/index>
   ModbusTk <external-docs/volttron-lib-modbustk-driver/docs/source/index>

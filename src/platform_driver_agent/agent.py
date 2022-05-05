"""
Agent documentation goes here.
For a quick tutorial on Agent Development, see https://volttron.readthedocs.io/en/develop/developing-volttron/developing-agents/agent-development.html#agent-development
"""

import datetime
import logging
import sys
from pprint import pformat

from volttron import utils
from volttron.client.messaging.health import STATUS_GOOD
from volttron.client.vip.agent import RPC, Agent, Core, PubSub
from volttron.client.vip.agent.subsystems.query import Query
from volttron.utils.commands import vip_main

# from . import __version__
__version__ = "0.1.0"

# Setup logging so that it runs within the platform
utils.setup_logging()

# The logger for this agent is _log and can be used throughout this file.
_log = logging.getLogger(__name__)


def platform_driver_agent(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: PlatformDriverAgent
    :rtype: PlatformDriverAgent
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return PlatformDriverAgent(setting1, setting2, **kwargs)


class PlatformDriverAgent(Agent):
    """
    PlatformDriverAgent is an example file that listens to the message bus and prints it to the log.
    """

    def __init__(self, setting1=1, setting2="some/random/topic", **kwargs):
        super(PlatformDriverAgent, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2
        # Runtime limit allows the agent to stop automatically after a specified number of seconds.
        self.runtime_limit = 0

        self.default_config = {"setting1": setting1, "setting2": setting2}
        # Set a default configuration to ensure that self.configure is called immediately to setup
        # the agent.
        self.vip.config.set_default("config", self.default_config)
        # Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = str(config["setting2"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2
        self.runtime_limit = int(config.get('runtime_limit', 0))

        self._set_runtime_limit()
        self._create_subscriptions(self.setting2)

    def _set_runtime_limit(self):
        if not self.runtime_limit and self.runtime_limit > 0:
            stop_time = datetime.datetime.now() + datetime.timedelta(seconds=self.runtime_limit)
            _log.info('PlatformDriverAgent agent will stop at {}'.format(stop_time))
            self.core.schedule(stop_time, self.core.stop)
        else:
            _log.info(
                'No valid runtime_limit configured; PlatformDriverAgent agent will run until manually stopped'
            )

    def _create_subscriptions(self, topic):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub', prefix=topic, callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        pass

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        # Example publish to pubsub
        # self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        # Example RPC call
        # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        pass

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.vip.rpc.call
        """
        return self.setting1 + arg1 - arg2

    @PubSub.subscribe('pubsub', '', all_platforms=True)
    def on_match(self, peer, sender, bus, topic, headers, message):
        """Use match_all to receive all messages and print them out."""
        self._logfn("Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
                    "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))


def main():
    """
    Main method called during startup of agent.
    :return:
    """
    try:
        vip_main(platform_driver_agent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2020, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}
"""Configuration for the pytest test suite."""

import json
import contextlib
from datetime import datetime

import pytest

from volttrontesting.fixtures.volttron_platform_fixtures import volttron_instance
from volttrontesting.platformwrapper import PlatformWrapper
from volttron.platform_driver.agent import PlatformDriverAgent
from volttrontesting.utils import AgentMock
from volttron.client.vip.agent import Agent

PlatformDriverAgent.__bases__ = (AgentMock.imitate(Agent, Agent()), )


class MockedInstance:

    def revert_all(self):
        pass


@contextlib.contextmanager
def pdriver(override_patterns: set = set(),
            override_interval_events: dict = {},
            patterns: dict = None,
            scalability_test: bool = None,
            waiting_to_finish: set = None,
            current_test_start: datetime = None):
    driver_config = json.dumps({
        "driver_scrape_interval": 0.05,
        "publish_breadth_first_all": False,
        "publish_depth_first": False,
        "publish_breadth_first": False
    })

    if scalability_test:
        platform_driver_agent = PlatformDriverAgent(driver_config,
                                                    scalability_test=scalability_test)
    else:
        platform_driver_agent = PlatformDriverAgent(driver_config)

    platform_driver_agent._override_patterns = override_patterns
    platform_driver_agent.instances = {"campus/building1/": MockedInstance()}
    platform_driver_agent.core.spawn_return_value = None
    platform_driver_agent._override_interval_events = override_interval_events
    platform_driver_agent._cancel_override_events_return_value = None
    platform_driver_agent.vip.config.set.return_value = ""

    if patterns is not None:
        platform_driver_agent._override_patterns = patterns
    if waiting_to_finish is not None:
        platform_driver_agent.waiting_to_finish = waiting_to_finish
    if current_test_start is not None:
        platform_driver_agent.current_test_start = current_test_start

    try:
        yield platform_driver_agent
    finally:
        platform_driver_agent.vip.reset_mock()
        platform_driver_agent._override_patterns.clear()


@pytest.fixture()
def publish_agent(volttron_instance):
    assert volttron_instance.is_running()
    return volttron_instance.build_agent(identity="publish_agent")

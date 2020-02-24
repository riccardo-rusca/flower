# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for Flower ClientManager."""


from flower.client import Client, NetworkClient
from flower.client_manager import SimpleClientManager


def test_simple_client_manager_register():
    """Tests if the register method works correctly"""
    # Prepare
    cid = "1"
    client = NetworkClient(cid=cid)
    client_manager = SimpleClientManager()

    # Execute
    first = client_manager.register(client)
    second = client_manager.register(client)

    # Assert
    assert first
    assert not second
    assert len(client_manager) == 1


def test_simple_client_manager_unregister():
    """Tests if the unregister method works correctly"""
    # Prepare
    cid = "1"
    client = NetworkClient(cid=cid)
    client_manager = SimpleClientManager()
    client_manager.register(client)

    # Execute
    client_manager.unregister(client)

    # Assert
    assert len(client_manager) == 0


def test_criteria_applied():
    """Test client sampling according to criteria."""
    # Prepare
    client1 = NetworkClient(cid="train_client_1")
    client2 = NetworkClient(cid="train_client_2")
    client3 = NetworkClient(cid="test_client_1")
    client4 = NetworkClient(cid="test_client_2")

    client_manager = SimpleClientManager()
    client_manager.register(client1)
    client_manager.register(client2)
    client_manager.register(client3)
    client_manager.register(client4)

    def criteria_is_test_client(client: Client) -> bool:
        return client.cid.startswith("test_")

    # Execute
    sampled_clients = client_manager.sample(2, criteria=criteria_is_test_client)

    # Assert
    assert client3 in sampled_clients
    assert client4 in sampled_clients


def test_criteria_not_applied():
    """Test client sampling according to criteria."""
    # Prepare
    client1 = NetworkClient(cid="train_client_1")
    client2 = NetworkClient(cid="train_client_2")
    client3 = NetworkClient(cid="test_client_1")
    client4 = NetworkClient(cid="test_client_2")

    client_manager = SimpleClientManager()
    client_manager.register(client1)
    client_manager.register(client2)
    client_manager.register(client3)
    client_manager.register(client4)

    # Execute
    sampled_clients = client_manager.sample(4)

    # Assert
    assert client1 in sampled_clients
    assert client2 in sampled_clients
    assert client3 in sampled_clients
    assert client4 in sampled_clients
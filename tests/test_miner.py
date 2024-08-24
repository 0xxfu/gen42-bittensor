import asyncio
import sys
import unittest
import bittensor as bt

from coding.protocol import StreamCodeSynapse
from neurons.miner import Miner


class TestMiner(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1] + [
            "--interpreter",
            "python3",
            "--name",
            "minertest",
            "--netuid",
            "171",
            "--subtensor.network",
            "test",
            "--wallet.name",
            "minertest",
            "--wallet.hotkey",
            "minertest",
            "--neuron.model_id",
            "deepseek-coder",
            "--axon.port",
            "8091",
            "--logging.debug",
            "--miner.name",
            "openai",
        ]
        self.miner = Miner()

    def test_forward(self):
        asyncio.run(self.async_forward())

    async def async_forward(self):

        synapse = StreamCodeSynapse(query="hello, who are you")
        with self.miner as miner:
            response = miner.forward(synapse=synapse)

            loop = asyncio.get_event_loop()

            async def mock_receive():
                pass

            async def mock_send(message):
                bt.logging.info(f"message: {message}")

            loop.run_until_complete(response({}, mock_receive, mock_send))

        self.miner.should_exit = True

    def test_run(self):
        self.miner.run()

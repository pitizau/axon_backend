import unittest
from agents.base_agent import BaseAgent

class TestBaseAgent(unittest.TestCase):
    """Unit tests for the BaseAgent class."""

    def test_initialization(self):
        """Tests that the BaseAgent can be initialized."""
        agent = BaseAgent(
            model_name="test-model",
            project="test-project",
            location="test-location"
        )
        self.assertEqual(agent.model_name, "test-model")
        self.assertEqual(agent.project, "test-project")
        self.assertEqual(agent.location, "test-location")

    def test_run_method(self):
        """Tests that the run method raises a NotImplementedError."""
        agent = BaseAgent(
            model_name="test-model",
            project="test-project",
            location="test-location"
        )
        with self.assertRaises(NotImplementedError):
            agent.run()

if __name__ == "__main__":
    unittest.main()
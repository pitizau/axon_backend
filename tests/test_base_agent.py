import unittest
from agents.base_agent import BaseAgent

class TestBaseAgent(unittest.TestCase):
    """Unit tests for the BaseAgent class."""

    def test_initialization(self):
        """Tests that the BaseAgent can be initialized."""
        agent = BaseAgent(
            model_name="test-model",
            project="test-project",
            # Corrected location to a valid GCP region
            location="us-central1"
        )
        self.assertEqual(agent.model_name, "test-model")
        self.assertEqual(agent.project, "test-project")
        # Corrected location
        self.assertEqual(agent.location, "us-central1")

    def test_run_method(self):
        """Tests that the run method raises a NotImplementedError."""
        agent = BaseAgent(
            model_name="test-model",
            project="test-project",
            # Corrected location to a valid GCP region
            location="us-central1"
        )
        with self.assertRaises(NotImplementedError):
            agent.run()

if __name__ == "__main__":
    unittest.main()
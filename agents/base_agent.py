import logging
from google.cloud import aiplatform

class BaseAgent:
    """The base class for all agents in the system."""

    def __init__(self, model_name: str, project: str, location: str):
        """
        Initializes the BaseAgent.

        Args:
            model_name: The name of the Vertex AI model to use.
            project: The GCP project ID.
            location: The GCP region.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.project = project
        self.location = location
        self.model_name = model_name
        self.model = self._initialize_model()

    def _initialize_model(self):
        """Initializes the Vertex AI model."""
        try:
            aiplatform.init(project=self.project, location=self.location)
            # This is a placeholder for the actual model initialization
            # In a real application, you would initialize the model here
            # For example:
            # from vertexai.preview.generative_models import GenerativeModel
            # return GenerativeModel(self.model_name)
            self.logger.info(f"Successfully initialized model: {self.model_name}")
            return self.model_name # Returning the name for now
        except Exception as e:
            self.logger.error(f"Failed to initialize model: {e}")
            raise

    def run(self, *args, **kwargs):
        """
        The main method to run the agent's logic.
        This should be implemented by the subclasses.
        """
        raise NotImplementedError("The 'run' method must be implemented by the subclass.")

    def _execute_prompt(self, prompt: str) -> str:
        """
        Executes a prompt against the configured Vertex AI model.

        Args:
            prompt: The prompt to execute.

        Returns:
            The response from the model.
        """
        self.logger.info(f"Executing prompt: {prompt[:100]}...")
        # This is a placeholder for the actual prompt execution
        # In a real application, you would send the prompt to the model and get a response
        # For example:
        # response = self.model.generate_content(prompt)
        # return response.text
        return f"This is a dummy response for the prompt: {prompt[:100]}..."
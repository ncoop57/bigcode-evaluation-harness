# This template file is adapted from: https://github.com/EleutherAI/lm-evaluation-harness/blob/master/templates/new_task.py

# TODO: Remove all TODO comments once the implementation is complete.
"""
TODO: Add the Paper Title on this line.
TODO: Add the paper's PDF URL (preferably from arXiv) on this line.
TODO: Write a Short Description of the task.
Homepage: TODO: Add the URL to the task's Homepage here.
"""
from bigcode_eval.base import Task
from bigcode_eval.tasks.custom_metrics.screenshot_similarity import compute_screenshot_similarity
from PIL import Image
from playwright.sync_api import sync_playwright
import io

# TODO: Add the BibTeX citation for the task.
_CITATION = """
"""


class WebSight(Task):
    DATASET_PATH = "HuggingFaceM4/WebSight"
    DATASET_NAME = None

    def __init__(self):
        super().__init__(
            # TODO: Specify the list of stop words in `stop_words` for the code generation task \
            # and if the evaluation requires executing the generated code in `requires_execution`.
            stop_words=["</html>"],
            requires_execution=False,
        )

    def get_dataset(self):
        # TODO: retrieve the evaluation subset from the loaded dataset (e.g. `self.dataset["test"]`)
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        return self.dataset["train"]

    def get_prompt(self, doc):
        # TODO: build the prompt for the language model from a sample `doc` from the dataset
        """
        Builds the prompt for the LM to generate from.
        :param doc: dict[str: str]
            sample from the test dataset
        :return: str
        """
        return "<html>"

    def get_reference(self, doc):
        # TODO: get the reference solution from a sample `doc` from the dataset
        """
        Builds the reference solution for the doc (sample from the test dataset).
        :param doc: dict[str: str]
            sample from the test dataset
        :return: str
        """
        return ""

    def postprocess_generation(self, generation, idx):
        # TODO: define the postprocessing for the LM generation
        """
        Defines the postprocessing for a LM generation.
        :param generation: str
            code generation from LM
        :param idx: int (if needed)
            index of doc in the dataset to which the generation belongs
        :return: str
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0"
                        " Safari/537.36"
                    )
                )
                page = context.new_page()
                page.set_content(generation)
                page.wait_for_load_state("networkidle")
                screenshot_bytes = page.screenshot(full_page=True)
                image = Image.open(io.BytesIO(screenshot_bytes))

                context.close()
                browser.close()
        except Exception:
            # Create a black image of a specific size (e.g., 960x960)
            image = Image.new('RGB', (960, 960), color = 'black')
        return image

    def process_results(self, generations, references):
        # TODO: define how the evaluation score is computed from list of \
        # generations and reference solutions
        """
        Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations as in {"metric_name": result}.
        We encourage to directly load the metric from `evaluate` library to keep the code concise.
        :param generations: list(Image)
            list of lists containing generations
        :param references: list(Image)
            list of str containing refrences
        :return: dict[str: float]
        """
        results = compute_screenshot_similarity(generations, references)
        return results

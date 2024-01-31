# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""
"""

from imgutils.metrics import lpips_difference
import numpy as np

_CITATION = """
"""

_DESCRIPTION = """
"""


_KWARGS_DESCRIPTION = """
"""

_LICENSE = """
"""

def compute_screenshot_similarity(predictions, references):
    """Returns the scores"""

    diffs = []
    for pred, ref in zip(predictions, references):
        diff = lpips_difference(pred, ref)
        diffs.append(diff)
    
    diffs = np.array(diffs)
    return {
        "mean": diffs.mean(),
        "median": np.median(diffs),
        "max": diffs.max(),
        "min": diffs.min(),
        "std": diffs.std(),
    }

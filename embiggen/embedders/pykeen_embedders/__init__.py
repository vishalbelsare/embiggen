"""Module with graph embedding models based on PyKeen."""
from ...utils import build_init, AbstractEmbeddingModel

build_init(
    module_library_names=["torch", "pykeen"],
    formatted_library_name="PyKeen",
    expected_parent_class=AbstractEmbeddingModel
)
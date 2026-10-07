import pytest

from quiz_module import clean_json_block


def test_clean_json_block_without_markdown():
    json_text = """
    {
        "questions": []
    }
    """

    result = clean_json_block(json_text)

    assert result.startswith("{")
    assert result.endswith("}")


def test_clean_json_block_with_json_fence():
    json_text = """```json
{
    "questions": []
}
```"""

    result = clean_json_block(json_text)

    assert result == """{
    "questions": []
}"""


def test_clean_json_block_with_plain_fence():
    json_text = """```
{
    "questions": []
}
```"""

    result = clean_json_block(json_text)

    assert result == """{
    "questions": []
}"""


def test_clean_json_block_removes_spaces():
    json_text = """
    
    ```json
    
    {
        "questions": []
    }
    
    ```
    
    """

    result = clean_json_block(json_text)

    assert result.startswith("{")
    assert result.endswith("}")


def test_clean_json_block_is_string():
    result = clean_json_block('{"questions": []}')

    assert isinstance(result, str)
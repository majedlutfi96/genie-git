"""Test the AI handler module."""

from pytest_mock import MockerFixture

from genie_git.ai_handler import suggest_commit_message


def test_generate_commit_message(mocker: MockerFixture) -> None:
    """Test generate_commit_message returns the correct commit message."""
    mock_client_instance = mocker.MagicMock()
    mock_response_instance = mocker.MagicMock()
    mock_response_instance.text = "feat: new feature"
    mock_client_instance.models.generate_content.return_value = mock_response_instance
    mocker.patch("genie_git.ai_handler.genai.Client", return_value=mock_client_instance)

    api_key = "test_key"
    git_logs = "test_logs"
    staged_changes = "test_changes"
    message_specifications = "concise and clear"

    response_text = suggest_commit_message(
        api_key,
        git_logs,
        staged_changes,
        message_specifications,
    )

    # To assure that the AI prompt includes the needed information
    call_kwargs = mock_client_instance.models.generate_content.call_args.kwargs
    prompt = call_kwargs["contents"]

    assert response_text == "feat: new feature"

    assert git_logs in prompt
    assert staged_changes in prompt
    assert message_specifications in prompt

    # To assure that the API key is used
    assert mock_client_instance.is_called_with(api_key=api_key)

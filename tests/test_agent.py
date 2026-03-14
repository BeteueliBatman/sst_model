from stt_agent.agent import STTCorrectionAgent
from stt_agent.config import Settings
from stt_agent.api import home


class FakeClient:
    def generate(self, **kwargs):
        assert kwargs["model"] == "test-model"
        return "დღეს სკოლაში წავედი."


def test_agent_corrects_text_with_client_response():
    agent = STTCorrectionAgent(
        settings=Settings(model_name="test-model"),
        client=FakeClient(),
    )

    result = agent.correct_text("dges skolshi wavedi")

    assert result.corrected_text == "დღეს სკოლაში წავედი."
    assert result.model == "test-model"


def test_agent_returns_empty_for_blank_text():
    agent = STTCorrectionAgent(
        settings=Settings(model_name="test-model"),
        client=FakeClient(),
    )

    result = agent.correct_text("   ")

    assert result.corrected_text == ""


def test_home_endpoint_payload_contains_demo_links():
    payload = home()

    assert payload["local_docs"] == "http://localhost:8000/docs"
    assert payload["local_health"] == "http://localhost:8000/health"
    assert payload["lan_docs"].endswith(":8000/docs")

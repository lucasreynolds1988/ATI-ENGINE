from core.vectorizer import vectorize_all

def test_vectorize():
    sample = "Hydraulic systems require regular pressure calibration."
    vectors = vectorize_all(sample)
    assert "openai_vector" in vectors
    assert "gemini_vector" in vectors
    assert "ollama_vector" in vectors
    print("✅ All vectors generated successfully.")

if __name__ == "__main__":
    test_vectorize()

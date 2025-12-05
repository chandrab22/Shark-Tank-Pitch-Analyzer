# SharkTank Pitch Analyzer (Modified)

This repository provides a **starter/demo version** of an assignment pipeline that evaluates pitch presentations. The system analyzes **audio features**, **tone/voice characteristics**, and **business content**, then generates **persona-specific feedback**.

This is a lightweight and reproducible implementation, meant as a skeleton for submission. Clear extension points are included so you can enhance the models or analysis modules later.

---

## Project Structure

- `src/`
  - `audio_analysis.py` – Extract audio features such as pitch, pauses, and energy
  - `emotion_detector.py` – Optional module to detect emotions/tone
  - `speech_to_text.py` – Converts audio to text transcription
  - `nlp_scoring.py` – Scores the business content in the transcript
  - `shark_agents.py` – Generates feedback from different persona perspectives
  - `integrate_pipeline.py` – Runs the full analysis pipeline
- `requirements.txt` – Lists required Python packages
- `sample_data/` – Place your `.wav` pitch files here
- `demo_outputs/` – Pipeline writes reports and transcripts here
- `pipeline_architecture.png` – (Optional) add a visual diagram of your pipeline
- `SharkTank_Pitch_Analyzer_Report.pdf` – Assignment report (submit separately)

---

## Usage Example

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

python src/integrate_pipeline.py --input sample_data/pitch1.wav --out demo_outputs/

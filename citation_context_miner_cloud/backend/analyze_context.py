from transformers import pipeline

# Load summarization and sentiment models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment = pipeline("sentiment-analysis")

def analyze_context(text_block):
    # ✅ Step 1: Truncate long text
    if len(text_block) > 1500:
        text_block = text_block[:1500]

    # ✅ Step 2: Try summarization safely
    try:
        summary = summarizer(
            text_block,
            max_length=80,
            min_length=20,
            truncation=True,
            do_sample=False
        )[0]['summary_text']
    except Exception as e:
        summary = f"⚠️ Summarization failed: {str(e)}"

    # ✅ Step 3: Try sentiment safely
    try:
        label = sentiment(text_block)[0]
        sentiment_label = label['label']
        confidence_score = label['score']
    except Exception as e:
        sentiment_label = "UNKNOWN"
        confidence_score = 0.0

    return {
        "summary": summary,
        "sentiment": sentiment_label,
        "confidence": confidence_score
    }


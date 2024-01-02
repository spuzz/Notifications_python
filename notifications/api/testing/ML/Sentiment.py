from transformers import pipeline
data = ["I love this", "I hate you"]
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

def sentiment_analysis(text_list: list[str]):

    scores = {"NEG": 0, "POS": 0, "NEU": 0}
    result = 0
    output = sentiment_pipeline(text_list)
    for i in output:
        score = i["score"]
        label = i["label"]
        scores[label] += score
    
    result = max(scores, key=scores.get)
    print(result)

    if result == "NEG":
        return "Negative Reaction"
    elif result == "POS":
        return "Positive Reaction"
    else:
        return "Neutral Reaction"
    
result = sentiment_pipeline(data)
test_result = sentiment_analysis(data)
print(result)
print(test_result)

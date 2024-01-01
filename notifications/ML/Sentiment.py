from transformers import pipeline
data = [" I really disagree with the content of this post. I belive the the client should really try to synthesize internal or ''organic'' sources before not after leveraging!", "I hate you"]
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
result = sentiment_pipeline(data)
print(result)
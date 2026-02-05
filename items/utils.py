from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_items(current_item, queryset, threshold=0.2):
    texts = []
    items = []

    current_text = f"{current_item.title} {current_item.description} {current_item.location}"
    texts.append(current_text)

    for item in queryset:
        text = f"{item.title} {item.description} {item.location}"
        texts.append(text)
        items.append(item)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    matched_items = []
    for item, score in zip(items, similarity_scores):
        if score >= threshold:
            matched_items.append(item)

    return matched_items

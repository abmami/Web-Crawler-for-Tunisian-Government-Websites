import json 
import spacy

def extract_sentences(paragraph):

    # Parse the paragraph using the French language model
    doc = nlp(paragraph)

    # Filter out sentences that are not complete
    complete_sentences = []
    sentences = [sent.text for sent in doc.sents]
    for sentence in sentences:
        tags = [token.pos_ for token in nlp(sentence)]
        if len(tags) >= 2 and tags[-1] == 'PUNCT' and (tags[-2] == 'NOUN' or tags[-2] == 'VERB'):
            complete_sentences.append(sentence.strip())

    return complete_sentences



if __name__ == '__main__':
    # load model for French language
    #python -m spacy download fr_core_news_sm
    nlp = spacy.load("fr_core_news_sm")

    # Read the paragraph from the file, and convert it to dictionary
    with open('./data/content.json', 'r', encoding='utf-8') as f:
        content = f.read()
        content = json.loads(content)
    
    # Extract sentences from the contents
    new_content = {}
    for k in content:
        filtered_sentences = extract_sentences(content[k])
        if filtered_sentences:
            new_content[k] = filtered_sentences

    with open('./data/filtered_content.json', 'w', encoding='utf-8') as f:
        json.dump(new_content, f, indent=4, ensure_ascii=False)
        print(len(new_content), 'contents filetered and saved to ./data/filtered_content.json')

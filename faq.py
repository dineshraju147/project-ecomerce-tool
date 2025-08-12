from pathlib import Path
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
chroma_client = chromadb.Client()
groq_client = Groq()
collection_name_faq = "faqs"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into ChromadDB...")
        collection = chroma_client.get_or_create_collection(
            name = collection_name_faq,
            embedding_function=ef,
        )
        df = pd.read_csv(path)
        docs = df['question'].tolist()
        metadata = [{'answer': ans} for ans in df['answer'].tolist()]
        ids = [f'id{i}' for i in range(len(docs))]

        collection.add(
            documents = docs,
            metadatas = metadata,
            ids = ids,
        )
        print(f'FAQ Data Successfully Ingested into Chroma collection: {collection.name}!:)')
    else:
        print(f"collection name {collection_name_faq} already exists!:(")

def get_relevent_qa(query):
    collection = chroma_client.get_collection(name = collection_name_faq)
    result = collection.query(
        query_texts = [query],
        n_results = 2
    )
    return result



def generate_answer(query, context):

    prompt = f'''Given the question and context below, generate the answer based on the context only.
    If you don't find the answer inside the context then say "I don't Know".
    Do not make things up.
    QUESTION: {query} 
    CONTEXT: {context}
    '''
    # call llm
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt ,
            }
        ],
        model= os.environ['GROQ_MODEL'],
    )

    return chat_completion.choices[0].message.content

def faq_chain(query):
    result = get_relevent_qa(query)
    context = ''.join([r.get("answer") for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer


if __name__ == "__main__":
    ingest_faq_data(faqs_path)
    # query = "Whats your policy on defective products?"
    query = "Do you take cash as a payment option?"
    #
    answer = faq_chain(query)
    print(answer)

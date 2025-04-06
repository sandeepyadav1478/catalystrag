from langchain_community.embeddings.ollama import OllamaEmbeddings

base_url='http://0.0.0.0:11434'
model='deepseek-r1:7b'


def get_embedding_function() -> object:
    embeddings = OllamaEmbeddings(
        model=model,
        base_url=base_url,
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def converter_to_embed(data) -> tuple:
    embeddings = get_embedding_function()
    # Convert text data to embeddings
    columns = data.columns.tolist()  # Replace 'text_column' with your CSV column name
    rows = data.values.tolist()[0]
    vectors = [embeddings._embed(title) for title in columns]

    return columns, rows, vectors
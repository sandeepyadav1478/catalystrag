from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path='./hw_200.csv',
    csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Index', 'Height', 'Weight']
})

data = loader.load()
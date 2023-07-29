import autodog

code = autodog.code('in.py')
engine = autodog.engine(
    api_key='PLEASE_ENTER_YOUR_KEY'
)
doc_model = autodog.doc_model(
    model_name="google style docstring"
)


code.insert_docs(engine, doc_model)

code.write(filepath='out.py')
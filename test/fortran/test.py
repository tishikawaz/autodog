import autodog

code = autodog.code('in.f90')
engine = autodog.engine(
    api_key='PLEASE_ENTER_YOUR_KEY',
    line_length = 80
)
doc_model = autodog.doc_model(
    model_name="google style docstring"
)

code.insert_docs(engine, doc_model)

code.write(filepath='out.f90')
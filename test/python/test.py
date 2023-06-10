import autodog

code = autodog.code('in.py')
engine = autodog.engine(api_key="PLEASE_ENTER_YOUR_KEY")

code.insert_docs(engine)

code.write(filepath='out.py')
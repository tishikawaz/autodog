import autodog

code = autodog.code('in.f90')
engine = autodog.engine(api_key="PLEASE_ENTER_YOUR_KEY")

code.insert_docs(engine)

code.write(filepath='out.f90')
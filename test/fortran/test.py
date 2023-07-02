import autodog

code = autodog.code('in.f90')
engine = autodog.engine(api_key='PLEASE_ENTER_YOUR_KEY', line_length = 80)

code.insert_docs(engine)

code.write(filepath='out.f90')
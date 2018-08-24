from ttrade import model

m = model.Model()
if not m.connection:
    print("no connection")
if not m.cursor:
    print("no cursor")

print("end of tests")
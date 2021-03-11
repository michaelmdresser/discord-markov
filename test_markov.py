import markovify
import sys

user_id = int(sys.argv[1])

model = None

with open("chains/%s" % user_id) as f:
    lines = f.readlines()[0]
    model = markovify.Text.from_json(lines)

for i in range(10):
    print(model.make_sentence())

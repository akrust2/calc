from flask import Flask, jsonify, request

app = Flask(__name__)
stacks = []


def find_next_id():
    if len(stacks) > 0:
        return max(stack["id"] for stack in stacks) + 1
    return 0

def getfromidx(idx):
    st = (stack for stack in stacks if stack["id"] == idx)
    try:
        first = next(st)
    except StopIteration:
        return None
    return first

@app.get("/rpn/stack")
def getstacks():
    if len(stacks) > 0:
        return jsonify(stacks)
    else:
        return "Empty stack, post a new stack",404

@app.post("/rpn/stack")
def poststack():
    idx = find_next_id()
    stack = {"id": idx, "stack": list()}
    stacks.append(stack)
    return jsonify(stack, 201);


@app.get("/rpn/stack/<int:idx>")
def getstack(idx):
    st = getfromidx(idx)
    if st is None :
        return "No such stack", 404
    return jsonify(stacks)

@app.post("/rpn/stack/<int:idx>")
def postvalue(idx):
    st = getfromidx(idx)
    if st is None :
        return "No such stack", 404

    st["stack"].append(request.json["value"])

    return jsonify(st), 200

@app.delete("/rpn/stack/<int:idx>")
def delete(idx):
    st = getfromidx(idx)
    if st is None:
        return "No such stack", 404
    stacks.remove(st[0])
    return "Successfully deleted stack", 204


def sum(a, b):
    return a+b

def prod(a,b):
    return a*b


def sub(a,b):
    return a-b

def div(a,b):
    return a/b


@app.post("/rpn/op/<oper>/stack/<int:idx>")
def postop(oper, idx):
    st = getfromidx(idx)
    if st is None:
        return "No such stack", 404
    if len(st) < 2 :
        return "Not enough operands in the stack", 409

    if oper not in ["add", "prod", "sub", "div"]:
        return "Unknown operand", 404

    a = st["stack"].pop()
    b = st["stack"].pop()

    res = 0
    if oper == "add":
        res = sum(a,b)
    elif oper == "sub":
        res = sub(a, b)
    elif oper == "prod":
        res = prod(a, b)
    elif oper == "div":
        res = div(a, b)

    st["stack"].append(res)
    return jsonify(st), 200



if __name__ == '__main__':
    app.run()  # run our Flask app
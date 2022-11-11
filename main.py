from http.client import HTTPException

import collections
from fastapi import FastAPI, Query
from pydantic import BaseModel
import json
from flask import Flask, request, render_template, redirect, url_for
from typing import Optional
app = FastAPI()

class Todo(BaseModel):
    id: Optional[int]=None
    name: str
    description: str
    duedate: str
    status: str
    urgentcy: str

with open('todo.json', 'r') as f:
    todo = json.load(f)

@app.get('/todoitem/{t_id}' ,status_code=200)
def get_todo(t_id: int):
    todoitem = [t for t in todo if t['id'] == t_id]
    return todoitem[0] if len(todoitem) >0 else {}




@app.get('/search', status_code=200)
def search_todo(name: Optional[str] = Query(None, title="name", description="The TODOlist want to search"),
                status: Optional[str] = Query(None, title="status", description="Which is not finished/ finshed"),
                arrange: Optional[int] = Query(None, title="sort", description="Sort ascending or descending"),
                urgent: Optional[bool] = Query(None, title="urgent", description="The todolist which is urgent")
                ):

    if arrange == 0 :
        todosearch1 =[ t for t in todo if t['status']==status]
        todosearch1.sort(key=lambda t: t['id'], reverse=False)
    elif arrange == 1:
        todosearch1 = [t for t in todo if t['status'] == status]
        todosearch1.sort(key=lambda t: t['id'],reverse=True)
    if urgent is None:
        if name is None:
            if status is None:
                return todo
            else:
                return todosearch1
        else:
            todosearch2 = [t for t in todo if name.lower() in t['name'].lower() ]
            if status is None:
                return todosearch2
            else:
                combined = [t for t in todosearch1 if t in todosearch2]
                return combined
    else:
        if arrange == 0:
            todosearch3 = [t for t in todo if t['urgent'] == True]
            todosearch3.sort(key=lambda t: t['id'], reverse=False)
        elif arrange == 1:
            todosearch3 = [t for t in todo if t['urgent'] == True]
            todosearch3.sort(key=lambda t: t['id'], reverse=True)

        if name is None:
            combineurgentstatus = [t for t in todosearch1 if t in todosearch3]
            return combineurgentstatus
        elif status is None:
            todosearch2 = [t for t in todo if name.lower() in t['name'].lower()]
            combineurgentname = [ t for t in todosearch2 if t in todosearch3]
            return combineurgentname
        else:
            return todosearch3

@app.post('/addtodo', status_code=201)
def add_todo(todoitem: Todo):
    render_template("add.html")
    t_id = max([t['id'] for t in todo])+1
    tdname = request.form['name']
    tddes = request.form['description']
    tddue = request.form['duedate']
    tdstat = request.form['status']

    new_todo = {
        "id": t_id,
        "name": tdname,
        "description": tddes,
        "duedate": tddue,
        "status": tdstat
    }

    todo.append(new_todo)
    with open('todo.json', 'w') as f:
        json.dump(todo, f)
    return new_todo



@app.put('/changeItem', status_code =204)
def change_item(todoitem: Todo):
    new_item = {
        "id": todoitem.id,
        "name": todoitem.name,
        "description": todoitem.description,
        "duedate": todoitem.duedate,
        "status": todoitem.status
    }

    todoitem_list = [ t for t in todo if t['id']]
    if len(todoitem_list)>0:
        todo.remove(todoitem_list[0])
        todo.append(new_item)
        with open('todo.json', 'w') as f:
            json.dump(todo, f)
            return new_item
    else:
        return HTTPException(status_code = 404, detail = f"item with i")

@app.delete('/deleteitem/{t_id}', status_code= 204)
def delete_item(t_id: int):
    todoitem = [t for t in todo if t['id']==t_id]
    if len(todoitem)>0:
        todo.remove(todoitem[0])
        with open('todo.json', 'w') as f:
            json.dump(todo, f)
    else:
        raise HTTPException(status_code = 404, detail = f"This is null / {t_id}")




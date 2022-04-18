from src.todo import todo


def setup_routes(app):
    app.router.add_route('GET', '/', todo.index, name='index')
    app.router.add_route('GET', '/note/', todo.note)
    app.router.add_route('GET', '/detail/{note_id}', todo.detail)
    app.router.add_route('GET', '/done/{note_id}', todo.done_note)
    app.router.add_route('GET', '/delete/{note_id}', todo.delete_note)
    app.router.add_route('GET', '/tag/{note_id}', todo.tag)
    app.router.add_route('POST', '/note', todo.create_note)
    app.router.add_route('POST', '/tag/{note_id}', todo.create_tag)
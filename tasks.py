from invoke import task

@task
def watch(c):
    c.run("""watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='cookiecutter . --no-input -o generated -f' \
    {{cookiecutter.project_slug}}
    """)

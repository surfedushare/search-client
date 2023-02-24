from invoke import task, Collection

from configuration import create_configuration


@task
def run(ctx):
    ctx.run("python -m unittest discover --start-directory=tests --top-level-directory=.")


configuration = create_configuration()


test_collection = Collection("test", run)
test_collection.configure(configuration)


namespace = Collection(
    test_collection
)

from invoke import task, Collection

from configuration import create_configuration


@task(help={
    "test_case": "A dotted path to package, TestCase or TestCase method to test"
})
def run(ctx, test_case=None):
    args = test_case if test_case else "discover --start-directory=tests --top-level-directory=."
    ctx.run(f"python -m unittest {args}")


configuration = create_configuration()


test_collection = Collection("test", run)
test_collection.configure(configuration)


namespace = Collection(
    test_collection
)

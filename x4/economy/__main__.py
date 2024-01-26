from x4 import docs, templates
from x4.economy.index import Builder
from x4.economy.subsets import subsets
from x4.logs import configure_structlog_once

if __name__ == "__main__":
    configure_structlog_once()

    builder = Builder(
        output_directory=docs,
        templates_directory=templates,
        subsets=subsets(),
    )
    builder.main()

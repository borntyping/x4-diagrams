import jinja2

from x4 import docs, templates
from x4.economy.writers import Builder, GraphvizWriter, IndexWriter, PlotlyWriter
from x4.economy.groups import groups
from x4.logs import configure_structlog_once

if __name__ == "__main__":
    configure_structlog_once()

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates),
        undefined=jinja2.StrictUndefined,
    )

    builder = Builder(
        graphviz_writer=GraphvizWriter(docs, environment),
        plotly_writer=PlotlyWriter(docs),
        index_writer=IndexWriter(docs, environment),
    )

    builder.main(groups=groups())

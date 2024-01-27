from x4 import docs, templates
from x4.economy.writers import Builder, GraphvizWriter, IndexWriter, PlotlyWriter
from x4.economy.groups import groups
from x4.logs import configure_structlog_once

if __name__ == "__main__":
    configure_structlog_once()

    builder = Builder(
        graphviz_writer=GraphvizWriter(docs),
        plotly_writer=PlotlyWriter(docs),
        index_writer=IndexWriter(docs, templates),
    )

    builder.main(groups=groups())

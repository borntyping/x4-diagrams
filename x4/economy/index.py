import dataclasses
import pathlib
import typing

import jinja2
import structlog

from x4.economy.writers import Diagram, GraphvizWriter, PlotlyWriter
from x4.economy.economy import Economy

logger = structlog.get_logger(logger_name=__name__)


@dataclasses.dataclass(frozen=True)
class Builder:
    output_directory: pathlib.Path
    templates_directory: pathlib.Path
    subsets: typing.Mapping[str, typing.Sequence[Economy]]

    def all_diagrams(self) -> typing.Mapping[str, typing.Sequence[Diagram]]:
        return {k: list(self.group_diagrams(v)) for k, v in self.subsets.items()}

    def group_diagrams(self, economies: typing.Sequence[Economy]) -> typing.Iterable[Diagram]:
        graphviz_writer = GraphvizWriter(output_directory=self.output_directory)
        plotly_writer = PlotlyWriter(output_directory=self.output_directory)

        for economy in economies:
            yield graphviz_writer.render(economy)
            yield plotly_writer.render(economy)

    def main(self) -> pathlib.Path:
        diagram_groups = self.all_diagrams()
        loader = jinja2.FileSystemLoader(self.templates_directory)
        environment = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)
        template = environment.get_template("index.html")
        rendered = template.render(groups=diagram_groups)
        path = self.output_directory / "index.html"
        path.write_text(rendered)
        logger.warning("Rendered index", path=path)
        return path

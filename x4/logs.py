import dataclasses
import logging

import structlog


@dataclasses.dataclass()
class Drop:
    keys: set[str]

    def __call__(self, logger, method_name, event_dict):
        for key in self.keys:
            if key in event_dict:
                del event_dict[key]

        return event_dict


def configure_structlog_once():
    structlog.configure_once(
        processors=[
            structlog.processors.add_log_level,
            Drop({"level"}),
            structlog.dev.ConsoleRenderer(
                sort_keys=False,
                columns=[
                    structlog.dev.Column(
                        "logger_name",
                        structlog.dev.KeyValueColumnFormatter(
                            key_style=None,
                            value_style=structlog.dev.BLUE,
                            reset_style=structlog.dev.RESET_ALL,
                            value_repr=str,
                            width=8,
                            prefix="[",
                            postfix="]",
                        ),
                    ),
                    structlog.dev.Column(
                        "event",
                        structlog.dev.KeyValueColumnFormatter(
                            key_style=None,
                            value_style=structlog.dev.BRIGHT,
                            reset_style=structlog.dev.RESET_ALL,
                            value_repr=str,
                            width=30,
                        ),
                    ),
                    structlog.dev.Column(
                        "",
                        structlog.dev.KeyValueColumnFormatter(
                            key_style=structlog.dev.CYAN,
                            value_style=structlog.dev.MAGENTA,
                            reset_style=structlog.dev.RESET_ALL,
                            value_repr=str,
                        ),
                    ),
                ],
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )

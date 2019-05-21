import json
from json import JSONDecodeError
import optparse

from pepper.cli import PepperCli


class RawCommand(PepperCli):
    def __init__(self, command):
        self.command = command.split(" ")[1:]

        self.parser = optparse.OptionParser()
        self.parser.option_groups.extend(
            [self.add_globalopts(), self.add_tgtopts(), self.add_retcodeopts()]
        )
        super().__init__()

    def parse(self):
        options, args = self.parser.parse_args(args=self.command)

        client = options.client if not options.batch else "local_batch"
        low = {"client": client}

        if client.startswith("local"):
            if len(args) < 2:
                return "Command or target not specified"

            low["tgt_type"] = options.expr_form
            low["tgt"] = args.pop(0)
            low["fun"] = args.pop(0)
            low["batch"] = options.batch
            low["arg"] = args
        elif client.startswith("runner"):
            low["fun"] = args.pop(0)
            for arg in args:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    try:
                        low[key] = json.loads(value)
                    except JSONDecodeError:
                        low[key] = value
                else:
                    low.setdefault("arg", []).append(arg)
        elif client.startswith("wheel"):
            low["fun"] = args.pop(0)
            for arg in args:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    try:
                        low[key] = json.loads(value)
                    except JSONDecodeError:
                        low[key] = value
                else:
                    low.setdefault("arg", []).append(arg)
        elif client.startswith("ssh"):
            if len(self.args) < 2:
                return "Command or target not specified"

            low["tgt_type"] = options.expr_form
            low["tgt"] = args.pop(0)
            low["fun"] = args.pop(0)
            low["batch"] = options.batch
            low["arg"] = args
        else:
            return "Client not implemented: {0}".format(client)

        return [low]

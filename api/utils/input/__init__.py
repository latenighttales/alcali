from shlex import split
import json
from json import JSONDecodeError


class RawCommand:
    def __init__(self, command, client="local", posix=True, inline=False):
        # TODO: check shlex.quote, raw string, etc..
        if inline:
            self.command = split(command, posix=posix)
        else:
            self.command = split(command, posix=posix)[1:]
        self.options = {"expr_form": "glob"}
        self.client = client

    def parse(self):
        args = self.command

        if args[0].startswith("--client"):
            self.client = args[0].split("=")[1]
            args.pop(0)

        low = {"client": self.client}

        if self.client.startswith("local"):
            if len(args) < 2:
                return "Command or target not specified"

            # Batch option
            low["batch"] = None
            if self.client == "local_batch":
                batch_index = None
                for index, arg in enumerate(args):
                    if arg in ["-b", "--batch", "--batch-size"]:
                        low["batch"] = args[index + 1]
                        batch_index = index
                if batch_index:
                    args.pop(batch_index)
                    args.pop(batch_index)
            # Timeout option
            timeout_index = None
            for index, arg in enumerate(args):
                if arg in ["-t", "--timeout"]:
                    low["timeout"] = int(args[index + 1])
                    timeout_index = index
            if timeout_index:
                args.pop(timeout_index)
                args.pop(timeout_index)

            # take care of targeting.
            target_dict = {
                "pcre": ["-E", "--pcre"],
                "list": ["-L", "--list"],
                "grain": ["-G", "--grain"],
                "grain_pcre": ["--grain-pcre"],
                "pillar": ["-I", "--pillar"],
                "pillar_pcre": ["--pillar-pcre"],
                "range": ["-R", "--range"],
                "compound": ["-C", "--compound"],
                "nodegroup": ["-N", "--nodegroup"],
            }
            for key, value in target_dict.items():
                if args[0] in value:
                    self.options["expr_form"] = key
                    args.pop(0)

            low["tgt_type"] = self.options["expr_form"]
            low["tgt"] = args.pop(0)
            low["fun"] = args.pop(0)
            low["arg"] = args

        elif self.client.startswith("runner") or self.client.startswith("wheel"):
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

        else:
            # This should never happen
            return "Client not implemented: {0}".format(self.client)

        return [low]

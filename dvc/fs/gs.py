import threading

from funcy import cached_property, wrap_prop

from dvc.scheme import Schemes

# pylint:disable=abstract-method
from .fsspec_wrapper import CallbackMixin, ObjectFSWrapper


class GSFileSystem(CallbackMixin, ObjectFSWrapper):
    scheme = Schemes.GS
    REQUIRES = {"gcsfs": "gcsfs"}
    PARAM_CHECKSUM = "etag"

    def _prepare_credentials(self, **config):
        return {
            "consistency": None,
            "project": config.get("projectname"),
            "token": config.get("credentialpath"),
        }

    @wrap_prop(threading.Lock())
    @cached_property
    def fs(self):
        from gcsfs import GCSFileSystem

        return GCSFileSystem(**self.fs_args)

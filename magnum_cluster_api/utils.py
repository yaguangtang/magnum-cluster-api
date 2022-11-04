import shortuuid
from magnum import objects as magnum_objects
from magnum.common import exception
from oslo_utils import strutils
from tenacity import retry, retry_if_exception_type

from magnum_cluster_api import objects


@retry(retry=retry_if_exception_type(exception.Conflict))
def generate_cluster_api_name(api, cluster):
    name = f"{cluster.name}-{shortuuid.uuid()[:10].lower()}"
    if (
        objects.Cluster.objects(api)
        .filter(namespace="magnum-system")
        .get_or_none(name=name)
        is not None
    ):
        raise exception.Conflict("Generated name already exists")
    return name


def get_cluster_label_as_bool(
    cluster: magnum_objects.Cluster, key: str, default: bool
) -> bool:
    value = get_cluster_label(cluster, key, default)
    return strutils.bool_from_string(value, strict=True)


def get_cluster_label_as_int(
    cluster: magnum_objects.Cluster, key: str, default: int
) -> int:
    value = get_cluster_label(cluster, key, default)
    return strutils.validate_integer(value, key)


def get_cluster_label(cluster: magnum_objects.Cluster, key: str, default: str) -> str:
    return cluster.labels.get(
        key, get_cluster_template_label(cluster.cluster_template, key, default)
    )


def get_cluster_template_label(
    cluster_template: magnum_objects.ClusterTemplate, key: str, default: str
) -> str:
    return cluster_template.labels.get(key, default)

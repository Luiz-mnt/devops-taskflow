"""Calcula o SHA256 da configuracao real de uma unica imagem Docker save."""

import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path


def image_config_id(archive_path: Path, repo_tag: str | None = None) -> str:
    with tarfile.open(archive_path, mode="r:*") as archive:
        manifests = [item for item in archive if item.name == "manifest.json"]
        if len(manifests) != 1 or not manifests[0].isfile():
            raise ValueError("O archive deve conter um unico manifest.json regular.")
        with archive.extractfile(manifests[0]) as manifest_file:
            manifest = json.load(manifest_file)
        if not isinstance(manifest, list) or len(manifest) != 1:
            raise ValueError("O archive deve descrever exatamente uma imagem.")
        entry = manifest[0]
        if not isinstance(entry, dict):
            raise ValueError("Entrada de manifest.json invalida.")
        tags = entry.get("RepoTags") or []
        if not isinstance(tags, list) or (
            repo_tag is not None and repo_tag not in tags
        ):
            raise ValueError("A tag esperada nao esta vinculada a imagem do archive.")
        config_path = entry.get("Config")
        if not isinstance(config_path, str):
            raise ValueError("Caminho Config ausente no manifesto.")
        config_match = re.fullmatch(
            r"(?:blobs/sha256/([a-f0-9]{64})|([a-f0-9]{64})\.json)", config_path
        )
        if config_match is None:
            raise ValueError("Config deve conter um nome SHA256 Docker ou OCI valido.")
        named_digest = next(value for value in config_match.groups() if value)
        configs = [item for item in archive.getmembers() if item.name == config_path]
        if len(configs) != 1 or not configs[0].isfile():
            raise ValueError("O archive deve conter uma unica Config regular.")
        if configs[0].size > 16 * 1024 * 1024:
            raise ValueError("Config excede o limite de 16 MiB.")
        with archive.extractfile(configs[0]) as config_file:
            config_bytes = config_file.read()
        actual_digest = hashlib.sha256(config_bytes).hexdigest()
        if actual_digest != named_digest:
            raise ValueError("O SHA256 dos bytes Config difere do nome no manifesto.")
        if not isinstance(json.loads(config_bytes), dict):
            raise ValueError("Config nao e um objeto JSON de configuracao de imagem.")
        return f"sha256:{actual_digest}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Docker archive .tar ou .tar.gz")
    parser.add_argument("--repo-tag", help="Exige a tag informada em RepoTags")
    arguments = parser.parse_args()
    try:
        print(image_config_id(arguments.archive, arguments.repo_tag))
        return 0
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())

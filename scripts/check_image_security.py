"""Aplica o gate HIGH/CRITICAL corrigivel ao inventario completo do Trivy."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument(
        "--expected-image-id",
        "--expected-config-id",
        dest="expected_image_id",
        required=True,
        help="SHA256 independente dos bytes Config do docker save, nao o OCI index ID",
    )
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    try:
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", arguments.expected_image_id):
            raise ValueError("O ID esperado deve ser um SHA256 Config valido.")
        report = json.loads(arguments.report.read_text(encoding="utf-8"))
        if report.get("ArtifactType") != "container_image":
            raise ValueError("O relatorio nao descreve uma imagem de container.")
        image_id = report.get("Metadata", {}).get("ImageID")
        if image_id != arguments.expected_image_id:
            raise ValueError(
                "A Config analisada difere da Config salva para publicacao."
            )
        results = report.get("Results")
        if not isinstance(results, list) or not results:
            raise ValueError("Inventario Trivy ausente ou vazio.")

        severity_counts = Counter()
        blocking = []
        unfixed = []
        for result in results:
            if result.get("Status") == "failure":
                raise ValueError("O inventario contem uma analise malsucedida.")
            vulnerabilities = result.get("Vulnerabilities") or []
            if not isinstance(vulnerabilities, list):
                raise ValueError("A lista de vulnerabilidades e invalida.")
            for vulnerability in vulnerabilities:
                severity = vulnerability.get("Severity", "UNKNOWN")
                if severity not in {"UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"}:
                    raise ValueError("Severidade desconhecida no inventario Trivy.")
                severity_counts[severity] += 1
                if severity not in {"HIGH", "CRITICAL"}:
                    continue
                finding = {
                    "target": result.get("Target"),
                    "id": vulnerability.get("VulnerabilityID"),
                    "package": vulnerability.get("PkgName"),
                    "installed": vulnerability.get("InstalledVersion"),
                    "fixed": vulnerability.get("FixedVersion"),
                    "severity": severity,
                }
                if vulnerability.get("FixedVersion"):
                    blocking.append(finding)
                else:
                    unfixed.append(finding)

        summary = {
            "image_config_id": image_id,
            "policy": "Block every HIGH/CRITICAL vulnerability with a fixed version",
            "severity_counts": dict(severity_counts),
            "blocking_count": len(blocking),
            "blocking_findings": blocking,
            "unfixed_high_critical_count": len(unfixed),
            "unfixed_high_critical": unfixed,
            "passed": not blocking,
        }
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1 if blocking else 0
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())

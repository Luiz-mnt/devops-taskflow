"""Falha controlada, a ser corrigida antes de integrar o projeto."""


def test_ci_bloqueia_falha_controlada():
    assert 1 == 0, "Demonstracao controlada: o CI deve bloquear esta alteracao."

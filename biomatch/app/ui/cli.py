from typing import Dict, List

from rich.console import Console
from rich.table import Table


console = Console()


def print_no_match():
    console.print("[bold red]Aucun match fiable trouvé.[/bold red]")


def print_match_results(results: List[Dict]):
    """Print top-K results returned by matching.score_candidates.

    Each result is a dict with keys: id, full_name, score, face_score, voice_score, meta.
    """
    table = Table(title="Résultats de recherche (Top-K)")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("Nom", style="green")
    table.add_column("Score", justify="right")
    table.add_column("Face", justify="right")
    table.add_column("Voix", justify="right")

    for idx, res in enumerate(results, start=1):
        table.add_row(
            str(idx),
            str(res.get("id", "?")),
            res.get("full_name", "N/A"),
            f"{res.get('score', 0.0):.3f}",
            f"{res.get('face_score', 0.0):.3f}",
            f"{res.get('voice_score', 0.0):.3f}",
        )

    console.print(table)

    # Show details for the top-1
    best = results[0]
    meta = best.get("meta", {})
    console.print("\n[bold]Détails meilleure correspondance[/bold]")
    for k in ["full_name", "email", "phone", "address", "notes"]:
        if k in meta and meta[k]:
            console.print(f"- {k}: {meta[k]}")
        elif k == "full_name" and best.get("full_name"):
            console.print(f"- full_name: {best['full_name']}")
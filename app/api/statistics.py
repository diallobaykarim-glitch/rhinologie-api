from collections import Counter
from html import escape

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.consultation import Consultation
from app.models.endoscopy import EndoscopyExam
from app.models.patient import Patient

router = APIRouter(prefix="/statistics", tags=["statistics"])


def _distribution(rows: list[tuple[str | int | None, int]]) -> dict[str, int]:
    return {str(key if key is not None else "unknown"): count for key, count in rows}


def _bar_svg(title: str, data: dict[str, int], width: int = 760, height: int = 320) -> str:
    if not data:
        return f"<h2>{escape(title)}</h2><p>Aucune donnee.</p>"

    margin_left = 180
    margin_right = 40
    margin_top = 48
    row_height = 38
    chart_height = max(height, margin_top + row_height * len(data) + 32)
    max_value = max(data.values()) or 1
    bar_width_max = width - margin_left - margin_right

    parts = [
        f'<svg class="chart" viewBox="0 0 {width} {chart_height}" role="img" aria-label="{escape(title)}">',
        f'<text x="0" y="26" class="chart-title">{escape(title)}</text>',
    ]
    for index, (label, value) in enumerate(data.items()):
        y = margin_top + index * row_height
        bar_width = int((value / max_value) * bar_width_max)
        parts.append(f'<text x="0" y="{y + 21}" class="axis-label">{escape(label)}</text>')
        parts.append(f'<rect x="{margin_left}" y="{y}" width="{bar_width}" height="24" rx="4"></rect>')
        parts.append(f'<text x="{margin_left + bar_width + 8}" y="{y + 18}" class="value-label">{value}</text>')
    parts.append("</svg>")
    return "".join(parts)


def _metric_card(label: str, value: str) -> str:
    return f'<section class="metric"><span>{escape(label)}</span><strong>{escape(value)}</strong></section>'


@router.get("")
def get_statistics(db: Session = Depends(get_db)):
    total_patients = db.scalar(select(func.count(Patient.id))) or 0
    total_consultations = db.scalar(select(func.count(Consultation.id))) or 0
    total_endoscopy = db.scalar(select(func.count(EndoscopyExam.id))) or 0
    avg_smell = db.scalar(select(func.avg(Consultation.smell_score)))
    avg_obstruction = db.scalar(select(func.avg(Consultation.nasal_obstruction_score)))

    sex_rows = db.execute(select(Patient.sex, func.count(Patient.id)).group_by(Patient.sex)).all()
    diagnosis_rows = db.execute(
        select(Consultation.diagnosis, func.count(Consultation.id))
        .group_by(Consultation.diagnosis)
        .order_by(func.count(Consultation.id).desc())
    ).all()
    polyp_rows = db.execute(
        select(EndoscopyExam.polyp_grade, func.count(EndoscopyExam.id))
        .group_by(EndoscopyExam.polyp_grade)
        .order_by(EndoscopyExam.polyp_grade)
    ).all()
    side_rows = db.execute(select(EndoscopyExam.side, func.count(EndoscopyExam.id)).group_by(EndoscopyExam.side)).all()

    high_obstruction = db.scalar(
        select(func.count(Consultation.id)).where(Consultation.nasal_obstruction_score >= 7)
    ) or 0
    low_smell = db.scalar(select(func.count(Consultation.id)).where(Consultation.smell_score <= 4)) or 0

    return {
        "totals": {
            "patients": total_patients,
            "consultations": total_consultations,
            "endoscopy_exams": total_endoscopy,
        },
        "averages": {
            "smell_score": round(float(avg_smell), 2) if avg_smell is not None else None,
            "nasal_obstruction_score": round(float(avg_obstruction), 2) if avg_obstruction is not None else None,
        },
        "clinical_flags": {
            "nasal_obstruction_score_gte_7": high_obstruction,
            "smell_score_lte_4": low_smell,
        },
        "distributions": {
            "sex": _distribution(sex_rows),
            "diagnosis": _distribution(diagnosis_rows),
            "polyp_grade": _distribution(polyp_rows),
            "endoscopy_side": _distribution(side_rows),
        },
    }


@router.get("/graphs", response_class=HTMLResponse)
def get_graphs(db: Session = Depends(get_db)):
    stats = get_statistics(db)
    diagnosis = stats["distributions"]["diagnosis"]
    top_diagnosis = dict(Counter(diagnosis).most_common(8))

    html = f"""
    <!doctype html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Statistiques Rhinologie</title>
      <style>
        body {{
          margin: 0;
          font-family: Arial, sans-serif;
          background: #f5f7f8;
          color: #1f2933;
        }}
        main {{
          max-width: 1040px;
          margin: 0 auto;
          padding: 32px 20px;
        }}
        h1 {{
          margin: 0 0 20px;
          font-size: 30px;
        }}
        .metrics {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 12px;
          margin-bottom: 24px;
        }}
        .metric {{
          background: #ffffff;
          border: 1px solid #d8e0e5;
          border-radius: 8px;
          padding: 16px;
        }}
        .metric span {{
          display: block;
          color: #52616b;
          font-size: 13px;
          margin-bottom: 8px;
        }}
        .metric strong {{
          font-size: 26px;
        }}
        .panel {{
          background: #ffffff;
          border: 1px solid #d8e0e5;
          border-radius: 8px;
          padding: 20px;
          margin-bottom: 16px;
          overflow-x: auto;
        }}
        .chart {{
          width: 100%;
          min-width: 620px;
        }}
        rect {{
          fill: #2d7d8f;
        }}
        .chart-title {{
          font-size: 20px;
          font-weight: 700;
          fill: #1f2933;
        }}
        .axis-label, .value-label {{
          font-size: 14px;
          fill: #334e5c;
        }}
      </style>
    </head>
    <body>
      <main>
        <h1>Statistiques Rhinologie</h1>
        <div class="metrics">
          {_metric_card("Patients", str(stats["totals"]["patients"]))}
          {_metric_card("Consultations", str(stats["totals"]["consultations"]))}
          {_metric_card("Endoscopies", str(stats["totals"]["endoscopy_exams"]))}
          {_metric_card("Obstruction moyenne", str(stats["averages"]["nasal_obstruction_score"]))}
          {_metric_card("Odorat moyen", str(stats["averages"]["smell_score"]))}
        </div>
        <div class="panel">{_bar_svg("Sexe des patients", stats["distributions"]["sex"])}</div>
        <div class="panel">{_bar_svg("Diagnostics principaux", top_diagnosis)}</div>
        <div class="panel">{_bar_svg("Grades de polypose", stats["distributions"]["polyp_grade"])}</div>
        <div class="panel">{_bar_svg("Cote endoscopique", stats["distributions"]["endoscopy_side"])}</div>
      </main>
    </body>
    </html>
    """
    return HTMLResponse(html)

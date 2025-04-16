from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive_analysis import HiveAnalysis
from schemas.hive_analysis import HiveAnalysisCreate, HiveAnalysisResponse
from core.auth import require_access

router = APIRouter(prefix = '/hive_analyses', tags = ['Hive Analyses'])

# Rota de criação de análise da colmeia
@router.post('/create', response_model = HiveAnalysisResponse, status_code = status.HTTP_201_CREATED)
def create_hive_analysis(hive_analysis: HiveAnalysisCreate, db: Session = Depends(get_db), user = Depends(require_access("owner", "manager"))):

    new_hive_analysis = HiveAnalysis(
        hive_id = hive_analysis.hive_id,
        user_id = hive_analysis.user_id,
        image_path = hive_analysis.image_path,
        varroa_detected = hive_analysis.varroa_detected,
        detection_confidence = hive_analysis.detection_confidence
    )

    db.add(new_hive_analysis)
    db.commit()
    db.refresh(new_hive_analysis)

    return {"message": "Análise da colmeia realizada com sucesso pelo usuário {user.name}"}

# Rota que mostra os dados da análise da colmeia
@router.get('/{hive_analysis_id}', response_model = HiveAnalysisResponse)
def get_hive_analysis(hive_analysis_id: int, db: Session = Depends(get_db), user = Depends(require_access("owner", "manager", "employee"))):
    hive_analysis = db.query(HiveAnalysis).filter(HiveAnalysis.id == hive_analysis_id).first()

    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Análise da colmeia não encontrada.')
    
    return hive_analysis

# Rota para deletar a análise da colmeia
@router.delete('/{hive_analysis_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_hive_analysis(hive_analysis_id: int, db: Session = Depends(get_db), user = Depends(require_access("owner", "manager"))):
    hive_analysis = db.query(HiveAnalysis).filter(HiveAnalysis.id == hive_analysis_id).first()

    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Análise de colmeia não encontrada.')
    
    db.delete(hive_analysis)
    db.commit()

    return {'message': f'Análise de colmeia deletada com sucesso pelo usuário {user.name}!'}
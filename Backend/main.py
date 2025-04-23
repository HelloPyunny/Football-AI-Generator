from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List

# 모델 import
from prediction_model.predict_position_grouped import predict_position_grouped
from prediction_model.predict_position import predict_new_player_position
from prediction_model.predict_ovr import predict_ovr_by_position

# 포메이션 관련 함수
from formation_gernerator.select_eleven import select_eleven_players
from formation_gernerator.optimal_team_formation import main_optimized
from visualization.visualize_formation import plot_formation

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 모델 ----------
class NewPlayerStats(BaseModel):
    stats: Dict[str, Dict[str, float]]

class SquadStats(BaseModel):
    players: List[str]
# --------------------------

# ---------- 개별 예측 ----------
@app.post("/predict")
def predict_endpoint(new_player_stats: NewPlayerStats):
    stats = new_player_stats.stats
    name_pg, pos_group = predict_position_grouped(stats)
    name_pos, detailed_pos = predict_new_player_position(stats)
    inner_stats = stats[list(stats.keys())[0]]
    overall = predict_ovr_by_position(inner_stats, detailed_pos)

    return {
        "player": name_pg,
        "predicted_position_grouped": pos_group,
        "predicted_position": detailed_pos,
        "OVR": overall
    }
# -------------------------------

# ---------- 포메이션 추천 ----------
@app.post("/predict/formation")
def formation_only(squad_stats: SquadStats):
    if len(squad_stats.players) != 11:
        return JSONResponse(content={"error": "Exactly 11 players required."}, status_code=400)

    try:
        result = main_optimized(squad_stats.players)
        return {
            "formation": result["formation"],
            "total_OVR": result["total_OVR"],
            "assignments": result["assignments"],
            "all_formations": result["all_formations"]
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
# ----------------------------------------------
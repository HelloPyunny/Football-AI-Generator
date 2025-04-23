import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64

def plot_formation(assignment, formation_name):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title(f"Best Formation: {formation_name}", fontsize=16, pad=15)

    # 경기장 배경
    field = patches.Rectangle((0, 0), 100, 100, linewidth=1, edgecolor='green', facecolor='#e0ffe0')
    ax.add_patch(field)

    # 포지션 라벨별 좌표 설정
    POS_COORDS = {
        "GK": (50, 5), "CB": (35, 25), "CB2": (65, 25), "LB": (15, 35), "RB": (85, 35),
        "CDM": (50, 40), "CM": (40, 50), "CM2": (60, 50), "LM": (20, 55), "RM": (80, 55),
        "CAM": (50, 60), "LW": (25, 70), "RW": (75, 70), "ST": (50, 80)
    }

    used_pos_count = {}

    for a in assignment:
        pos = a["position"]
        name = a["player"]
        ovr = a["ovr"]

        # 중복 포지션은 pos2, pos3 식으로 처리
        count = used_pos_count.get(pos, 0)
        used_pos_count[pos] = count + 1
        label = pos if count == 0 else f"{pos}{count+1}"
        coord = POS_COORDS.get(label, POS_COORDS.get(pos, (50, 50)))

        # 원 그리기
        circle = plt.Circle(coord, 4, color='blue', alpha=0.4)
        ax.add_patch(circle)
        ax.text(coord[0], coord[1], f"{name}\n({ovr})", fontsize=7, ha='center', va='center')

    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
